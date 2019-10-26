import pathlib
import typing
import cv2
import numpy as np
from loguru import logger

from stagesepx.cutter import VideoCutRange
from stagesepx import toolbox
from stagesepx import constants
from stagesepx.hook import BaseHook, GreyHook, CompressHook
from stagesepx.video import VideoObject, VideoFrame


class SingleClassifierResult(object):
    def __init__(self, video_path: str, frame_id: int, timestamp: float, stage: str):
        self.video_path = video_path
        self.frame_id = frame_id
        self.timestamp = timestamp
        self.stage = stage

    def to_dict(self) -> typing.Dict:
        return self.__dict__

    def __str__(self):
        return f"<ClassifierResult stage={self.stage} frame_id={self.frame_id} timestamp={self.timestamp}>"

    __repr__ = __str__


class ClassifierResult(object):
    def __init__(self, data: typing.List[SingleClassifierResult]):
        self.video_path = data[0].video_path
        self.data = data

    def get_timestamp_list(self) -> typing.List[float]:
        return [each.timestamp for each in self.data]

    def get_stage_list(self) -> typing.List[str]:
        return [each.stage for each in self.data]

    def get_stage_set(self) -> typing.Set[str]:
        return set(self.get_stage_list())

    def get_offset(self) -> float:
        # timestamp offset between frames
        return self.data[1].timestamp - self.data[0].timestamp

    def get_specific_stage(
        self, stage_name: str
    ) -> typing.List[SingleClassifierResult]:
        """ get specific stage range by stage name """
        return sorted(
            [i for i in self.data if i.stage == stage_name],
            key=lambda x: x.frame_id,
        )

    def get_length(self) -> int:
        return len(self.data)

    def calc_changing_cost(
        self
    ) -> typing.Dict[str, typing.Tuple[SingleClassifierResult, SingleClassifierResult]]:
        """ calc time cost between stages """
        # add changing cost
        cost_dict: typing.Dict[
            str, typing.Tuple[SingleClassifierResult, SingleClassifierResult]
        ] = {}
        i = 0
        while i < len(self.data) - 1:
            cur = self.data[i]
            next_one = self.data[i + 1]

            # next one is changing
            if next_one.stage == constants.UNSTABLE_FLAG:
                for j in range(i + 1, len(self.data)):
                    i = j
                    next_one = self.data[j]
                    if next_one.stage != constants.UNSTABLE_FLAG:
                        break

                changing_name = f"{cur.stage} - {next_one.stage}"
                cost_dict[changing_name] = (cur, next_one)
            else:
                i += 1
        return cost_dict


class BaseClassifier(object):
    def __init__(
        self,
        compress_rate: float = None,
        target_size: typing.Tuple[int, int] = None,
        *args,
        **kwargs,
    ):
        # default compress rate is 0.2
        if (not compress_rate) and (not target_size):
            logger.debug(
                f"no compress rate or target size received. set compress rate to 0.2"
            )
            compress_rate = 0.2

        self.compress_rate = compress_rate
        self.target_size = target_size
        logger.debug(f"compress rate: {self.compress_rate}")
        logger.debug(f"target size: {self.target_size}")

        self._data: typing.Dict[str, typing.Union[typing.List[pathlib.Path]]] = dict()

        # init inner hooks
        self._hook_list: typing.List[BaseHook] = list()
        compress_hook = CompressHook(
            overwrite=True, compress_rate=compress_rate, target_size=target_size
        )
        grey_hook = GreyHook(overwrite=True)
        self.add_hook(compress_hook)
        self.add_hook(grey_hook)

    def add_hook(self, new_hook: BaseHook):
        """
        add a hook

        :param new_hook:
        :return:
        """
        self._hook_list.append(new_hook)
        logger.debug(f"add hook: {new_hook.__class__.__name__}")

    def load(
        self, data: typing.Union[str, typing.List[VideoCutRange], None], *args, **kwargs
    ):
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
        raise TypeError(f"data type error, should be str or typing.List[VideoCutRange]")

    def load_from_list(
        self, data: typing.List[VideoCutRange], frame_count: int = None, *_, **__
    ):
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
            logger.debug(
                f"stage [{stage_name}] found, and got {len(stage_pic_list)} pics"
            )

    def read(self, *args, **kwargs):
        for stage_name, stage_data in self._data.items():
            if isinstance(stage_data[0], pathlib.Path):
                yield stage_name, self.read_from_path(stage_data, *args, **kwargs)
            else:
                raise TypeError(
                    f"data type error, should be str or typing.List[VideoCutRange]"
                )

    @staticmethod
    def read_from_path(data: typing.List[pathlib.Path], *_, **__):
        return (toolbox.imread(each.as_posix()) for each in data)

    def read_from_list(
        self, data: typing.List[int], video_cap: cv2.VideoCapture = None, *_, **__
    ):
        raise DeprecationWarning("this function already deprecated")

    def _classify_frame(self, frame: VideoFrame, *args, **kwargs) -> str:
        """ must be implemented by sub class """

    def _apply_hook(
        self, frame_id: int, frame: np.ndarray, *args, **kwargs
    ) -> np.ndarray:
        for each_hook in self._hook_list:
            frame = each_hook.do(frame_id, frame, *args, **kwargs)
        return frame

    def classify(
        self,
        video: typing.Union[str, VideoObject],
        limit_range: typing.List[VideoCutRange] = None,
        step: int = None,
        *args,
        **kwargs,
    ) -> ClassifierResult:
        """
        start classification

        :param video: path to target video or VideoObject
        :param limit_range: frames in these range will be ignored
        :param step: step between frames, default to 1
        :param args:
        :param kwargs:
        :return:
        """
        logger.debug(f"classify with {self.__class__.__name__}")

        if not step:
            step = 1

        final_result: typing.List[SingleClassifierResult] = list()
        if isinstance(video, str):
            video = VideoObject(video)

        operator = video.get_operator()
        frame = operator.get_frame_by_id(1)
        while frame is not None:
            if limit_range:
                if not any([each.contain(frame.frame_id) for each in limit_range]):
                    logger.debug(
                        f"frame {frame.frame_id} ({frame.timestamp}) not in target range, skip"
                    )
                    final_result.append(
                        SingleClassifierResult(
                            video.path, frame.frame_id, frame.timestamp, "-1"
                        )
                    )
                    frame = operator.get_frame_by_id(frame.frame_id + step)
                    continue

            # hook
            frame.data = self._apply_hook(frame.frame_id, frame.data, *args, **kwargs)

            result = self._classify_frame(frame, *args, **kwargs)
            logger.debug(
                f"frame {frame.frame_id} ({frame.timestamp}) belongs to {result}"
            )

            final_result.append(
                SingleClassifierResult(
                    video.path, frame.frame_id, frame.timestamp, result
                )
            )
            frame = operator.get_frame_by_id(frame.frame_id + step)
        return ClassifierResult(final_result)
