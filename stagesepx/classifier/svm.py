from loguru import logger
import cv2
import os
import pickle
import typing
import numpy as np
from sklearn.svm import LinearSVC

from stagesepx.classifier.base import BaseClassifier
from stagesepx import toolbox
from stagesepx.video import VideoFrame
from stagesepx import constants


class SVMClassifier(BaseClassifier):
    FEATURE_DICT = {
        "hog": toolbox.turn_hog_desc,
        "lbp": toolbox.turn_lbp_desc,
        # do not use feature transform
        "raw": lambda x: x,
    }
    UNKNOWN_STAGE_NAME = constants.UNKNOWN_STAGE_FLAG

    def __init__(
        self, feature_type: str = None, score_threshold: float = None, *args, **kwargs
    ):
        """
        init classifier

        :param feature_type:
            before training, classifier will convert pictures into feature, for better classification.
            eg: 'hog', 'lbp' or 'raw'
        :param score_threshold:
            float, 0 - 1.0, under this value, label -> UNKNOWN_STAGE_NAME
            default value is 0 (None)
        """
        super().__init__(*args, **kwargs)

        # feature settings
        if not feature_type:
            feature_type = "hog"
        if feature_type not in self.FEATURE_DICT:
            raise AttributeError(f"no feature func named {feature_type}")
        self.feature_func: typing.Callable = self.FEATURE_DICT[feature_type]
        logger.debug(f"feature function: {feature_type}")

        # model settings
        self._model: typing.Optional[LinearSVC] = None
        self.score_threshold: float = score_threshold or 0.0
        logger.debug(f"score threshold: {self.score_threshold}")

    def clean_model(self):
        self._model = None

    def save_model(self, model_path: str, overwrite: bool = None):
        """
        save trained model

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
        with open(model_path, "wb") as f:
            pickle.dump(self._model, f)

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

        # joblib raise an error ( i have no idea about how to fix it ) here, so use pickle instead
        with open(model_path, "rb") as f:
            self._model = pickle.load(f)

    def read_from_list(
        self, data: typing.List[int], video_cap: cv2.VideoCapture = None, *_, **__
    ):
        raise NotImplementedError("svm classifier only support loading data from files")

    def train(self):
        """
        train your classifier with data. must be called before prediction

        :return:
        """
        if not self._model:
            logger.debug("no model can be used. build a new one.")
            self._model = LinearSVC()
        else:
            logger.debug("already have a trained model. train on this model.")

        train_data = list()
        train_label = list()
        for each_label, each_label_pic_list in self.read():
            for each_pic_object in each_label_pic_list:
                logger.debug(f"training label: {each_label}")
                # apply hook
                each_pic_object = self._apply_hook(
                    VideoFrame(-1, -1.0, each_pic_object)
                )
                each_pic_object = each_pic_object.data

                each_pic_object = self.feature_func(each_pic_object).flatten()
                train_data.append(each_pic_object)
                train_label.append(each_label)
        logger.debug("data ready")

        assert (
            len(train_label) > 1
        ), f"seems only one class in the training dataset, at least two classes are required: {train_label}"
        self._model.fit(train_data, train_label)
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
        pic_object = self.feature_func(frame)
        pic_object = pic_object.reshape(1, -1)

        # scores for each stages
        # IMPORTANT:
        # these scores are not always precise
        # at the most of time, we used a tiny train data set for training
        # which may causes 'liblinear failed to converge'
        # actually, it can know which one is the target class
        # but the calculated value may becomes weird
        scores = self._model.decision_function(pic_object)[0]
        logger.debug(f"scores: {scores}")

        # in the binary case, return type is different (wtf ...)
        # for more effective i think
        if len(self._model.classes_) == 2:
            # scores is a float
            # confidence score for self.classes_[1] where >0 means this
            # class would be predicted
            return self._model.classes_[1 if scores > 0 else 0]

        # unknown
        if max(scores) < self.score_threshold:
            logger.warning(
                f"max score is lower than {self.score_threshold}, unknown class"
            )
            return self.UNKNOWN_STAGE_NAME

        return self._model.classes_[np.argmax(scores)]

    def _classify_frame(self, frame: VideoFrame, *_, **__) -> str:
        return self.predict_with_object(frame.data)
