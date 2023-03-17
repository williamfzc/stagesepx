from loguru import logger
import os
import cv2
import typing
import numpy as np
import pathlib

try:
    import tensorflow
except ImportError:
    raise ImportError("KerasClassifier requires tensorflow. install it first.")
from keras.preprocessing.image import ImageDataGenerator

# https://github.com/tensorflow/models/issues/6177
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K

from stagesepx.classifier.base import BaseModelClassifier
from stagesepx import toolbox
from stagesepx.video import VideoFrame
from stagesepx import constants


class KerasClassifier(BaseModelClassifier):
    UNKNOWN_STAGE_NAME = constants.UNKNOWN_STAGE_FLAG
    # https://github.com/williamfzc/stagesepx/issues/112
    MODEL_DENSE = 6

    def __init__(
        self,
        score_threshold: float = None,
        data_size: typing.Sequence[int] = None,
        nb_train_samples: int = None,
        nb_validation_samples: int = None,
        epochs: int = None,
        batch_size: int = None,
        *_,
        **__,
    ):
        super(KerasClassifier, self).__init__(*_, **__)

        # model
        self._model: typing.Optional[Sequential] = None
        # settings
        self.score_threshold: float = score_threshold or 0.0
        self.data_size: typing.Sequence[int] = data_size or (200, 200)
        self.nb_train_samples: int = nb_train_samples or 64
        self.nb_validation_samples: int = nb_validation_samples or 64
        self.epochs: int = epochs or 20
        self.batch_size: int = batch_size or 4

        logger.debug(f"score threshold: {self.score_threshold}")
        logger.debug(f"data size: {self.data_size}")
        logger.debug(f"nb train samples: {self.nb_train_samples}")
        logger.debug(f"nb validation samples: {self.nb_validation_samples}")
        logger.debug(f"epochs: {self.epochs}")
        logger.debug(f"batch size: {self.batch_size}")

    def clean_model(self):
        self._model = None

    def save_model(self, model_path: str, overwrite: bool = None):
        """
        save trained weights

        :param model_path:
        :param overwrite:
        :return:
        """
        logger.debug(f"save model to {model_path}")
        # assert model file
        if os.path.isfile(model_path) and not overwrite:
            raise FileExistsError(
                f"model file {model_path} already existed, you can set `overwrite` True to cover it"
            )
        # assert model data is not empty
        assert self._model, "model is empty"
        self._model.save_weights(model_path)

    def load_model(self, model_path: str, overwrite: bool = None):
        """
        load trained model

        :param model_path:
        :param overwrite:
        :return:
        """
        logger.debug(f"load model from {model_path}")
        # assert model file
        assert os.path.isfile(model_path), f"model file {model_path} not existed"
        # assert model data is empty
        if self._model and not overwrite:
            raise RuntimeError(
                f"model is not empty, you can set `overwrite` True to cover it"
            )
        self._model = self.create_model()
        self._model.load_weights(model_path)

    def create_model(self) -> Sequential:
        """model structure. you can overwrite this method to build your own model"""
        logger.info(f"creating keras sequential model")
        if K.image_data_format() == "channels_first":
            input_shape = (1, *self.data_size)
        else:
            input_shape = (*self.data_size, 1)

        model = Sequential()
        model.add(Conv2D(32, (3, 3), input_shape=input_shape))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Conv2D(32, (3, 3)))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Conv2D(64, (3, 3)))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Flatten())
        model.add(Dense(64))
        model.add(Activation("relu"))
        model.add(Dropout(0.5))
        model.add(Dense(self.MODEL_DENSE))

        model.add(Activation("softmax"))

        model.compile(
            loss="sparse_categorical_crossentropy",
            optimizer="rmsprop",
            metrics=["accuracy"],
        )
        logger.info("model created")
        return model

    def train(self, data_path: str = None, *_, **__):
        """
        train your classifier with data. must be called before prediction

        :return:
        """

        def _data_verify(p: str):
            p = pathlib.Path(p)
            assert p.is_dir(), f"{p} is not a valid directory"
            # validate: at least two classes
            number_of_dir = len([each for each in os.listdir(p) if (p / each).is_dir()])
            assert (
                number_of_dir > 1
            ), f"dataset only contains one class. maybe some path errors happened: {p}?"

            # more than 6 classes?
            # fake edit here
            assert number_of_dir <= self.MODEL_DENSE, (
                f"dataset has {number_of_dir} classes (more than " + str(self.MODEL_DENSE) + "), please see "
                f"https://github.com/williamfzc/stagesepx/issues/112 "
            )

        _data_verify(data_path)

        if not self._model:
            logger.debug("no model can be used. build a new one.")
            self._model = self.create_model()
        else:
            logger.debug("model found")

        datagen = ImageDataGenerator(
            rescale=1.0 / 16, shear_range=0.2, zoom_range=0.2, validation_split=0.33
        )

        train_generator = datagen.flow_from_directory(
            data_path,
            target_size=self.data_size,
            batch_size=self.batch_size,
            color_mode="grayscale",
            class_mode="sparse",
            subset="training",
        )

        validation_generator = datagen.flow_from_directory(
            data_path,
            target_size=self.data_size,
            batch_size=self.batch_size,
            color_mode="grayscale",
            class_mode="sparse",
            subset="validation",
        )

        self._model.fit(
            train_generator,
            epochs=self.epochs,
            validation_data=validation_generator,
        )

        logger.debug("train finished")

    def predict(self, pic_path: str, *args, **kwargs) -> str:
        """
        predict a single picture

        :param pic_path:
        :return:
        """
        pic_object = toolbox.imread(pic_path)
        # fake VideoFrame for apply_hook
        fake_frame = VideoFrame(0, 0.0, pic_object)
        fake_frame = self._apply_hook(fake_frame, *args, **kwargs)
        return self.predict_with_object(fake_frame.data)

    def predict_with_object(self, frame: np.ndarray) -> str:
        """
        predict a single object

        :param frame:
        :return:
        """
        # resize for model
        frame = cv2.resize(frame, dsize=self.data_size)
        frame = np.expand_dims(frame, axis=[0, -1])

        result = self._model.predict(frame)
        tag = str(np.argmax(result, axis=1)[0])
        confidence = result.max()
        logger.debug(f"confidence: {confidence}")
        if confidence < self.score_threshold:
            logger.warning(
                f"max score is lower than {self.score_threshold}, unknown class"
            )
            return self.UNKNOWN_STAGE_NAME
        return tag

    def _classify_frame(self, frame: VideoFrame, *_, **__) -> str:
        return self.predict_with_object(frame.data)
