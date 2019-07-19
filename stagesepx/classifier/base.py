import pathlib
import typing
import numpy as np
from loguru import logger

from stagesepx.cutter import VideoCutRange
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


class BaseClassifier(object):
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

    def _classify_frame(self, frame: np.ndarray, *args, **kwargs) -> str:
        raise NotImplementedError('must implement this function')

    def classify(self,
                 video_path: str,
                 limit_range: typing.List[VideoCutRange] = None,
                 step: int = None,
                 *args, **kwargs) -> typing.List[ClassifierResult]:
        logger.debug(f'classify with {self.__class__.__name__}')
        assert self.data, 'should load data first'

        if not step:
            step = 1

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

                result = self._classify_frame(frame, *args, **kwargs)
                logger.debug(f'frame {frame_id} ({frame_timestamp}) belongs to {result}')
                final_result.append(ClassifierResult(video_path, frame_id, frame_timestamp, result))
                toolbox.video_jump(cap, frame_id + step - 1)
                ret, frame = cap.read()
        return final_result
