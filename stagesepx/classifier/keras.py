from loguru import logger
import os
import cv2
import typing
import numpy as np

try:
    import tensorflow
except ImportError:
    raise ImportError("KerasClassifier requires tensorflow. install it first.")
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K

from stagesepx.classifier.base import BaseModelClassifier
from stagesepx import toolbox
from stagesepx.video import VideoFrame
from stagesepx import constants


class KerasClassifier(BaseModelClassifier):
    UNKNOWN_STAGE_NAME = constants.UNKNOWN_STAGE_FLAG

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
        self.nb_train_samples: int = nb_train_samples or 500
        self.nb_validation_samples: int = nb_validation_samples or 500
        self.epochs: int = epochs or 20
        self.batch_size: int = batch_size or 32

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
        """ model structure. you can overwrite this method to build your own model """
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
        model.add(Dense(6))
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

        self._model.fit_generator(
            train_generator,
            steps_per_epoch=self.nb_train_samples // self.batch_size,
            epochs=self.epochs,
            validation_data=validation_generator,
            validation_steps=self.nb_validation_samples // self.batch_size,
        )

        logger.debug("train finished")

    def predict(self, pic_path: str) -> str:
        """
        predict a single picture

        :param pic_path:
        :return:
        """
        pic_object = toolbox.imread(pic_path)
        return self.predict_with_object(pic_object)

    def predict_with_object(self, frame: np.ndarray) -> str:
        """
        predict a single object

        :param frame:
        :return:
        """
        # resize for model
        frame = cv2.resize(frame, dsize=self.data_size)
        frame = np.expand_dims(frame, axis=[0, -1])

        return str(self._model.predict_classes(frame)[0])

    def _classify_frame(self, frame: VideoFrame, *_, **__) -> str:
        return self.predict_with_object(frame.data)
