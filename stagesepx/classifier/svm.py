from loguru import logger
import cv2
import os
import pickle
import typing
import numpy as np
from sklearn.svm import LinearSVC

from stagesepx.classifier.base import BaseClassifier
from stagesepx import toolbox


class SVMClassifier(BaseClassifier):
    FEATURE_DICT = {
        'hog': toolbox.turn_hog_desc,
        # TODO not implemented
        # 'surf': toolbox.turn_surf_desc,

        # do not use feature transform
        'raw': lambda x: x,
    }

    def __init__(self, feature_type: str = None):
        super().__init__()

        if not feature_type:
            feature_type = 'hog'
        if feature_type not in self.FEATURE_DICT:
            raise AttributeError(f'no feature func named {feature_type}')
        self.feature_func = self.FEATURE_DICT[feature_type]
        self._model = None
        logger.debug(f'feature function: {feature_type}')

    def clean_model(self):
        self._model = None

    def save_model(self, model_path: str, overwrite: bool = None):
        logger.debug(f'save model to {model_path}')
        # assert model file
        if os.path.isfile(model_path) and not overwrite:
            raise FileExistsError(f'model file {model_path} already existed, you can set `overwrite` True to cover it')
        # assert model data is not empty
        assert self._model, 'model is empty'
        with open(model_path, 'wb') as f:
            pickle.dump(self._model, f)

    def load_model(self, model_path: str, overwrite: bool = None):
        logger.debug(f'load model from {model_path}')
        # assert model file
        assert os.path.isfile(model_path), f'model file {model_path} not existed'
        # assert model data is empty
        if self._model and not overwrite:
            raise RuntimeError(f'model is not empty, you can set `overwrite` True to cover it')

        # joblib raise an error ( i have no idea about how to fix it ) here, so use pickle instead
        with open(model_path, 'rb') as f:
            self._model = pickle.load(f)

    def read_from_list(self, data: typing.List[int], video_cap: cv2.VideoCapture = None, *_, **__):
        raise NotImplementedError('svm classifier only support loading data from files')

    def train(self):
        if not self._model:
            self._model = LinearSVC()

        train_data = list()
        train_label = list()
        for each_label, each_label_pic_list in self.read():
            for each_pic_object in each_label_pic_list:
                each_pic_object = toolbox.compress_frame(each_pic_object)
                each_pic_object = self.feature_func(each_pic_object).flatten()
                train_data.append(each_pic_object)
                train_label.append(each_label)
        logger.debug('data ready')
        self._model.fit(train_data, train_label)
        logger.debug('train finished')

    def predict(self, pic_path: str) -> str:
        pic_object = cv2.imread(pic_path)
        return self.predict_with_object(pic_object)

    def predict_with_object(self, pic_object: np.ndarray) -> str:
        pic_object = toolbox.compress_frame(pic_object)
        pic_object = self.feature_func(pic_object)
        pic_object = pic_object.reshape(1, -1)
        return self._model.predict(pic_object)[0]

    def _classify_frame(self,
                        frame: np.ndarray,
                        *_, **__) -> str:
        return self.predict_with_object(frame)
