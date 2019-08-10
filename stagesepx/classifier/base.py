import pathlib
import typing
import cv2
import numpy as np
from loguru import logger

from stagesepx.cutter import VideoCutRange
from stagesepx import toolbox
from stagesepx.hook import BaseHook


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
    def __init__(self,
                 compress_rate: float = None,
                 target_size: typing.Tuple[int, int] = None,
                 *args, **kwargs):
        self.compress_rate = compress_rate
        self.target_size = target_size
        logger.debug(f'compress rate: {self.compress_rate}')
        logger.debug(f'target size: {self.target_size}')

        self._data: typing.Dict[
            str,
            typing.Union[
                typing.List[pathlib.Path],
                typing.List[int],
            ]
        ] = dict()

        self._hook_list: typing.List[BaseHook] = list()

    def add_hook(self, new_hook: BaseHook):
        """
        add a hook

        :param new_hook:
        :return:
        """
        self._hook_list.append(new_hook)
        logger.debug(f'add hook: {new_hook.__class__.__name__}')

    def load(self, data: typing.Union[str, typing.List[VideoCutRange]], *args, **kwargs):
        """
        at most of time, you MUST load data (from cutter) before classification
        otherwise you need a trained model

        :param data: path to your cutter's result (mainly from pick_and_save)
        :param args:
        :param kwargs:
        :return:
        """
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

    def diff(self, another: 'BaseClassifier') -> typing.Dict[str, typing.Dict[str, float]]:
        assert another._data, 'must load data first'
        result_dict = dict()

        self_data = dict(self.read())
        for each_self_stage, each_self_data in self_data.items():
            another_data = dict(another.read())
            each_self_data_pic = next(each_self_data)

            each_stage_dict = dict()
            # compare with all the stages
            for each_another_stage, each_another_data in another_data.items():
                # compare with all the pictures in same stage, and pick the max one
                max_ssim = -1
                for each_pic in each_another_data:
                    ssim = toolbox.compare_ssim(
                        each_pic,
                        each_self_data_pic,
                    )
                    if ssim > max_ssim:
                        max_ssim = ssim
                each_stage_dict[each_another_stage] = max_ssim

            result_dict[each_self_stage] = each_stage_dict
        return result_dict

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
                        frame_id: int,
                        frame: np.ndarray,
                        video_cap: cv2.VideoCapture,
                        *args, **kwargs) -> str:
        raise NotImplementedError('must implement this function')

    def _apply_hook(self, frame_id: int, frame: np.ndarray, *args, **kwargs):
        for each_hook in self._hook_list:
            each_hook.do(frame_id, frame, *args, **kwargs)

    def classify(self,
                 video_path: str,
                 limit_range: typing.List[VideoCutRange] = None,
                 step: int = None,
                 *args, **kwargs) -> typing.List[ClassifierResult]:
        """
        start classification

        :param video_path: path to target video
        :param limit_range: frames in these range will be ignored
        :param step: step between frames, default to 1
        :param args:
        :param kwargs:
        :return:
        """
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

                # hook
                self._apply_hook(frame_id, frame, *args, **kwargs)

                result = self._classify_frame(frame_id, frame, cap, *args, **kwargs)
                logger.debug(f'frame {frame_id} ({frame_timestamp}) belongs to {result}')

                final_result.append(ClassifierResult(video_path, frame_id, frame_timestamp, result))
                toolbox.video_jump(cap, frame_id + step)
                ret, frame = cap.read()
        return final_result
