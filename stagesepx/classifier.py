import pathlib
import typing
import cv2
import os
import pickle
import numpy as np
from loguru import logger
from sklearn.svm import LinearSVC

from stagesepx import toolbox


class StageData(object):
    def __init__(self, name: str, pic_list: typing.List[str]):
        self.name = name
        self.pic_list = pic_list


class ClassifierResult(object):
    def __init__(self,
                 video_path: str,
                 frame_id: int,
                 timestamp: float,
                 stage: str):
        self.video_path = video_path
        self.frame_id = frame_id
        self.timestamp = timestamp
        self.stage = stage


class _BaseClassifier(object):
    def __init__(self):
        self.data: typing.Dict[str, typing.List[pathlib.Path]] = dict()

    def load(self, data_home: str):
        p = pathlib.Path(data_home)
        stage_dir_list = p.iterdir()
        for each in stage_dir_list:
            # load dir only
            if each.is_file():
                continue
            stage_name = each.name
            stage_pic_list = [i.absolute() for i in each.iterdir()]
            self.data[stage_name] = stage_pic_list
            logger.debug(f'stage [{stage_name}] found, and got {len(stage_pic_list)} pics')


class SSIMClassifier(_BaseClassifier):
    def classify(self, video_path: str, threshold: float = None) -> typing.List[ClassifierResult]:
        logger.debug(f'classify with {self.__class__.__name__}')
        assert self.data, 'should load data first'

        if not threshold:
            threshold = 0.85

        final_result: typing.List[ClassifierResult] = list()
        with toolbox.video_capture(video_path) as cap:
            ret, frame = cap.read()
            while ret:
                frame_id = toolbox.get_current_frame_id(cap)
                frame_timestamp = toolbox.get_current_frame_time(cap)
                frame = toolbox.compress_frame(frame)

                result = list()
                for each_stage_name, each_stage_pic_list in self.data.items():
                    each_result = list()
                    for each in each_stage_pic_list:
                        target_pic = cv2.imread(each.as_posix())
                        target_pic = toolbox.compress_frame(target_pic)
                        each_pic_ssim = toolbox.compare_ssim(frame, target_pic)
                        each_result.append(each_pic_ssim)
                    ssim = max(each_result)
                    result.append((each_stage_name, ssim))
                    logger.debug(f'stage [{each_stage_name}]: {ssim}')

                result = max(result, key=lambda x: x[1])
                if result[1] < threshold:
                    logger.debug('not a known stage, set it -1')
                    result = ('-1', result[1])
                logger.debug(f'frame {frame_id} ({frame_timestamp}) belongs to {result[0]}')

                final_result.append(ClassifierResult(video_path, frame_id, frame_timestamp, result[0]))
                ret, frame = cap.read()
        return final_result


class SVMClassifier(_BaseClassifier):
    def __init__(self):
        super().__init__()
        self._model = None

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
                each_pic_object = toolbox.compress_frame(each_pic_object).flatten()
                train_data.append(each_pic_object)
                train_label.append(each_label)
        logger.debug('data ready')
        self._model.fit(train_data, train_label)
        logger.debug('train finished')

    def predict(self, pic_path: str) -> str:
        pic_object = cv2.imread(pic_path)
        return self.predict_with_object(pic_object)

    def predict_with_object(self, pic_object: np.ndarray) -> str:
        pic_object = toolbox.compress_frame(pic_object).reshape(1, -1)
        return self._model.predict(pic_object)[0]

    def classify(self, video_path: str) -> typing.List[ClassifierResult]:
        logger.debug(f'classify with {self.__class__.__name__}')
        assert self.data, 'should load data first'
        assert self._model, 'should train before classify'

        final_result: typing.List[ClassifierResult] = list()
        with toolbox.video_capture(video_path) as cap:
            ret, frame = cap.read()
            while ret:
                frame_id = toolbox.get_current_frame_id(cap)
                frame_timestamp = toolbox.get_current_frame_time(cap)
                result = self.predict_with_object(frame)

                logger.debug(f'frame {frame_id} ({frame_timestamp}) belongs to {result}')

                final_result.append(ClassifierResult(video_path, frame_id, frame_timestamp, result))
                ret, frame = cap.read()
        return final_result


if __name__ == '__main__':
    s = SSIMClassifier()
    s.load('../1562999463')
    res = s.classify('../video/demo_video.mp4')
