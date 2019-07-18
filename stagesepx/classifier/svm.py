from loguru import logger
import typing
import cv2
import os
import pickle
import numpy as np
from sklearn.svm import LinearSVC

from stagesepx.classifier.base import BaseClassifier, ClassifierResult
from stagesepx.cutter import VideoCutRange
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

    def train(self):
        if not self._model:
            self._model = LinearSVC()

        train_data = list()
        train_label = list()
        for each_label, each_label_pic_list in self.data.items():
            for each_pic in each_label_pic_list:
                logger.debug(f'loading {each_pic} ...')
                each_pic_object = cv2.imread(each_pic.as_posix())
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

    def classify(self,
                 video_path: str,
                 limit_range: typing.List[VideoCutRange] = None) -> typing.List[ClassifierResult]:
        logger.debug(f'classify with {self.__class__.__name__}')
        assert self.data, 'should load data first'
        assert self._model, 'should train before classify'

        final_result: typing.List[ClassifierResult] = list()
        with toolbox.video_capture(video_path) as cap:
            ret, frame = cap.read()
            while ret:
                frame_id = toolbox.get_current_frame_id(cap)
                frame_timestamp = toolbox.get_current_frame_time(cap)
                if limit_range:
                    if not any([each.contain(frame_id) for each in limit_range]):
                        logger.debug(f'frame {frame_id} ({frame_timestamp}) not in target range, skip')
                        final_result.append(ClassifierResult(video_path, frame_id, frame_timestamp, '-1'))
                        ret, frame = cap.read()
                        continue

                result = self.predict_with_object(frame)
                logger.debug(f'frame {frame_id} ({frame_timestamp}) belongs to {result}')
                final_result.append(ClassifierResult(video_path, frame_id, frame_timestamp, result))
                ret, frame = cap.read()
        return final_result
