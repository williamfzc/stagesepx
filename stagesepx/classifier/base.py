import pathlib
import typing
import cv2
import numpy as np
from loguru import logger

from stagesepx.cutter import VideoCutRange
from stagesepx import toolbox


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
        self._data: typing.Dict[
            str,
            typing.Union[
                typing.List[pathlib.Path],
                typing.List[int],
            ]
        ] = dict()

    def load(self, data: typing.Union[str, typing.List[VideoCutRange]], *args, **kwargs):
        if isinstance(data, str):
            return self.load_from_dir(data, *args, **kwargs)
        if isinstance(data, list):
            return self.load_from_list(data, *args, **kwargs)
        raise TypeError(f'data type error, should be str or typing.List[VideoCutRange]')

    def load_from_list(self, data: typing.List[VideoCutRange], frame_count: int = None, *_, **__):
        for stage_name, stage_data in enumerate(data):
            target_frame_list = stage_data.pick(frame_count)
            self._data[str(stage_name)] = target_frame_list

    def load_from_dir(self, dir_path: str, *_, **__):
        p = pathlib.Path(dir_path)
        stage_dir_list = p.iterdir()
        for each in stage_dir_list:
            # load dir only
            if each.is_file():
                continue
            stage_name = each.name
            stage_pic_list = [i.absolute() for i in each.iterdir()]
            self._data[stage_name] = stage_pic_list
            logger.debug(f'stage [{stage_name}] found, and got {len(stage_pic_list)} pics')

    def read(self, *args, **kwargs):
        for stage_name, stage_data in self._data.items():
            if isinstance(stage_data[0], pathlib.Path):
                yield stage_name, self.read_from_path(stage_data, *args, **kwargs)
            elif isinstance(stage_data[0], int):
                yield stage_name, self.read_from_list(stage_data, *args, **kwargs)
            else:
                raise TypeError(f'data type error, should be str or typing.List[VideoCutRange]')

    @staticmethod
    def read_from_path(data: typing.List[pathlib.Path], *_, **__):
        return (cv2.imread(each.as_posix()) for each in data)

    def read_from_list(self, data: typing.List[int], video_cap: cv2.VideoCapture = None, *_, **__):
        cur_frame_id = toolbox.get_current_frame_id(video_cap)
        data = (toolbox.get_frame(video_cap, each) for each in data)
        toolbox.video_jump(video_cap, cur_frame_id)
        return data

    def _classify_frame(self,
                        frame: np.ndarray,
                        video_cap: cv2.VideoCapture,
                        *args, **kwargs) -> str:
        raise NotImplementedError('must implement this function')

    def classify(self,
                 video_path: str,
                 limit_range: typing.List[VideoCutRange] = None,
                 step: int = None,
                 *args, **kwargs) -> typing.List[ClassifierResult]:
        logger.debug(f'classify with {self.__class__.__name__}')
        assert self._data, 'should load data first'

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

                result = self._classify_frame(frame, cap, *args, **kwargs)
                logger.debug(f'frame {frame_id} ({frame_timestamp}) belongs to {result}')
                final_result.append(ClassifierResult(video_path, frame_id, frame_timestamp, result))
                toolbox.video_jump(cap, frame_id + step)
                ret, frame = cap.read()
        return final_result
