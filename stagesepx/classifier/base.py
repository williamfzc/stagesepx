import pathlib
import typing
from collections import OrderedDict
import os
import json
import cv2
import time
import numpy as np
from loguru import logger

from stagesepx.cutter import VideoCutRange
from stagesepx import toolbox
from stagesepx import constants
from stagesepx.hook import BaseHook, GreyHook, CompressHook
from stagesepx.video import VideoObject, VideoFrame


class SingleClassifierResult(object):
    def __init__(
        self,
        video_path: str,
        frame_id: int,
        timestamp: float,
        stage: str,
        data: np.ndarray = None,
    ):
        self.video_path: str = video_path
        self.frame_id: int = frame_id
        self.timestamp: float = timestamp
        self.stage: str = stage

        # optional
        self.data: np.ndarray = data

    def to_video_frame(self, *args, **kwargs) -> VideoFrame:
        # VideoFrame has `data`
        # SingleClassifierResult has `stage` (data is optional)

        # already have data
        if self.data is not None:
            return VideoFrame(self.frame_id, self.timestamp, self.data)
        # no data
        with toolbox.video_capture(self.video_path) as cap:
            frame = toolbox.get_frame(cap, self.frame_id)
            compressed = toolbox.compress_frame(frame, *args, **kwargs)
        return VideoFrame(self.frame_id, self.timestamp, compressed)

    def get_data(self) -> np.ndarray:
        return self.to_video_frame().data

    def is_stable(self) -> bool:
        return self.stage not in (
            constants.UNSTABLE_FLAG,
            constants.IGNORE_FLAG,
            constants.UNKNOWN_STAGE_FLAG,
        )

    def contain_image(
        self, *, image_path: str = None, image_object: np.ndarray = None, **kwargs
    ) -> typing.Dict[str, typing.Any]:
        return self.to_video_frame().contain_image(
            image_path=image_path, image_object=image_object, **kwargs
        )

    def to_dict(self) -> typing.Dict:
        return self.__dict__

    def __str__(self):
        return f"<ClassifierResult stage={self.stage} frame_id={self.frame_id} timestamp={self.timestamp}>"

    __repr__ = __str__


class ClassifierResult(object):
    LABEL_DATA: str = "data"
    LABEL_VIDEO_PATH: str = "video_path"

    def __init__(self, data: typing.List[SingleClassifierResult]):
        self.video_path: str = data[0].video_path
        self.data: typing.List[SingleClassifierResult] = data

    def get_timestamp_list(self) -> typing.List[float]:
        return [each.timestamp for each in self.data]

    def get_stage_list(self) -> typing.List[str]:
        return [each.stage for each in self.data]

    def get_length(self) -> int:
        return len(self.data)

    def get_offset(self) -> float:
        # timestamp offset between frames
        return self.data[1].timestamp - self.data[0].timestamp

    def get_stage_set(self) -> typing.Set[str]:
        return set(self.get_stage_list())

    def to_dict(
        self,
    ) -> typing.Dict[str, typing.List[typing.List[SingleClassifierResult]]]:
        stage_list = list(self.get_stage_set())
        try:
            int(stage_list[0])
        except ValueError:
            stage_list.sort()
        else:
            stage_list.sort(key=lambda o: int(o))

        d = OrderedDict()
        for each_stage in stage_list:
            d[each_stage] = self.get_specific_stage_range(each_stage)
        return d

    def contain(self, stage_name: str) -> bool:
        return stage_name in self.get_stage_set()

    def first(self, stage_name: str) -> SingleClassifierResult:
        for each in self.data:
            if each.stage == stage_name:
                logger.debug(f"first frame of {stage_name}: {each}")
                return each
        logger.warning(f"no stage named {stage_name} found")

    def last(self, stage_name: str) -> SingleClassifierResult:
        for each in self.data[::-1]:
            if each.stage == stage_name:
                logger.debug(f"last frame of {stage_name}: {each}")
                return each
        logger.warning(f"no stage named {stage_name} found")

    def get_stage_range(self) -> typing.List[typing.List[SingleClassifierResult]]:
        """
        return a range list.
        if your video has 30 frames, with 3 stages, this list can be:
        [(0, 1, ... 11), (12, 13 ... 20), (21, 22 ... 30)]

        :return:
        """
        result: typing.List[typing.List[SingleClassifierResult]] = []

        # real data
        cur = self.data[0]
        # frame id = index + 1
        cur_index = cur.frame_id - 1
        # init pointer
        ptr = cur_index
        length = self.get_length()
        while ptr < length:
            # next frame
            next_one = self.data[ptr]
            # is continuous?
            if cur.stage == next_one.stage:
                ptr += 1
                continue
            # +1 because:
            # [1,2,3,4,5][1:3] == [2,3]
            # -1 because:
            # current ptr is the next frame
            result.append(self.data[cur_index : ptr + 1 - 1] or [self.data[cur_index]])
            cur = next_one
            cur_index = next_one.frame_id - 1

        # issue #90
        assert len(result) > 0, "video seems to only contain one stage"

        last_data = self.data[-1]
        last_result = result[-1][-1]
        if last_result != last_data:
            result.append(
                self.data[last_result.frame_id - 1 + 1 : last_data.frame_id - 1 + 1]
                or [self.data[last_result.frame_id - 1]]
            )
        logger.debug(f"get stage range: {result}")
        return result

    def get_specific_stage_range(
        self, stage_name: str
    ) -> typing.List[typing.List[SingleClassifierResult]]:
        """ get specific stage range by stage name (maybe contains some partition """
        ret = list()
        for each_range in self.get_stage_range():
            cur = each_range[0]
            if cur.stage == stage_name:
                ret.append(each_range)
        return ret

    def get_not_stable_stage_range(
        self,
    ) -> typing.List[typing.List[SingleClassifierResult]]:
        unstable = self.get_specific_stage_range(constants.UNSTABLE_FLAG)
        ignore = self.get_specific_stage_range(constants.IGNORE_FLAG)
        return sorted(unstable + ignore, key=lambda x: x[0].stage)

    def mark_range(self, start: int, end: int, target_stage: str):
        for each in self.data[start:end]:
            each.stage = target_stage
        logger.debug(f"range {start} to {end} has been marked as {target_stage}")

    def mark_range_unstable(self, start: int, end: int):
        self.mark_range(start, end, constants.UNSTABLE_FLAG)

    def mark_range_ignore(self, start: int, end: int):
        self.mark_range(start, end, constants.IGNORE_FLAG)

    def time_cost_between(self, start_stage: str, end_stage: str) -> float:
        return self.first(end_stage).timestamp - self.last(start_stage).timestamp

    def get_important_frame_list(self) -> typing.List[SingleClassifierResult]:
        # save the first frame
        result = [self.data[0]]

        prev = self.data[0]
        for cur in self.data[1:]:
            if cur.stage != prev.stage:
                result.append(prev)
                result.append(cur)
            prev = cur

        # save the latest frame
        if result[-1] != self.data[-1]:
            result.append(self.data[-1])
        return result

    def calc_changing_cost(
        self,
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
            if not next_one.is_stable():
                for j in range(i + 1, len(self.data)):
                    i = j
                    next_one = self.data[j]
                    if next_one.is_stable():
                        break

                changing_name = f"from {cur.stage} to {next_one.stage}"
                cost_dict[changing_name] = (cur, next_one)
            else:
                i += 1
        return cost_dict

    def dumps(self) -> str:
        # for np.ndarray
        def _handler(obj: object):
            if isinstance(obj, np.ndarray):
                # ignore
                return "<np.ndarray object>"
            return obj.__dict__

        return json.dumps(self, sort_keys=True, default=_handler)

    def dump(self, json_path: str, **kwargs):
        logger.debug(f"dump result to {json_path}")
        assert not os.path.isfile(json_path), f"{json_path} already existed"
        with open(json_path, "w+", **kwargs) as f:
            f.write(self.dumps())

    @classmethod
    def load(cls, from_file: str) -> "ClassifierResult":
        assert os.path.isfile(from_file), f"file {from_file} not existed"
        with open(from_file, encoding=constants.CHARSET) as f:
            content = json.load(f)

        data = content[cls.LABEL_DATA]
        return ClassifierResult([SingleClassifierResult(**each) for each in data])

    # alias
    get_frame_length = get_offset


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
        raise NotImplementedError

    def _apply_hook(self, frame: VideoFrame, *args, **kwargs) -> VideoFrame:
        for each_hook in self._hook_list:
            frame = each_hook.do(frame, *args, **kwargs)
        return frame

    def classify(
        self,
        video: typing.Union[str, VideoObject],
        valid_range: typing.List[VideoCutRange] = None,
        step: int = None,
        keep_data: bool = None,
        boost_mode: bool = None,
        *args,
        **kwargs,
    ) -> ClassifierResult:
        """
        start classification

        :param video: path to target video or VideoObject
        :param valid_range: frames out of these ranges will be ignored
        :param step: step between frames, default to 1
        :param keep_data: default to False. if enabled, all the frames will contain numpy data.
        :param boost_mode:
        :param args:
        :param kwargs:
        :return:
        """
        logger.debug(f"classify with {self.__class__.__name__}")
        start_time = time.time()

        # default
        if not step:
            step = 1
        if boost_mode is None:
            boost_mode = True
        # check
        assert (boost_mode and valid_range) or (
            not (boost_mode or valid_range)
        ), "boost_mode required valid_range"

        final_result: typing.List[SingleClassifierResult] = list()
        if isinstance(video, str):
            video = VideoObject(video)

        operator = video.get_operator()
        frame = operator.get_frame_by_id(1)
        # for boost
        prev_result: typing.Optional[str] = None
        while frame is not None:
            # hook
            frame = self._apply_hook(frame, *args, **kwargs)
            # ignore some ranges
            if valid_range and not any(
                [each.contain(frame.frame_id) for each in valid_range]
            ):
                logger.debug(
                    f"frame {frame.frame_id} ({frame.timestamp}) not in target range, skip"
                )
                result = constants.IGNORE_FLAG
                # is changing
                prev_result = None
            else:
                # is continuous?
                if boost_mode and (prev_result is not None):
                    # do not classify again
                    result = prev_result
                # else, do the real job
                else:
                    prev_result = result = self._classify_frame(frame, *args, **kwargs)
                logger.debug(
                    f"frame {frame.frame_id} ({frame.timestamp}) belongs to {result}"
                )

            final_result.append(
                SingleClassifierResult(
                    video.path,
                    frame.frame_id,
                    frame.timestamp,
                    result,
                    frame.data if keep_data else None,
                )
            )
            frame = operator.get_frame_by_id(frame.frame_id + step)
        end_time = time.time()
        logger.debug(f"classifier cost: {end_time - start_time}")
        return ClassifierResult(final_result)


class BaseModelClassifier(BaseClassifier):
    # model
    def save_model(self, model_path: str, overwrite: bool = None):
        raise NotImplementedError

    def load_model(self, model_path: str, overwrite: bool = None):
        raise NotImplementedError

    def clean_model(self):
        raise NotImplementedError

    # actions
    def train(self, data_path: str = None, *_, **__):
        raise NotImplementedError

    def predict(self, pic_path: str) -> str:
        raise NotImplementedError

    def predict_with_object(self, frame: np.ndarray) -> str:
        raise NotImplementedError

    def read_from_list(
        self, data: typing.List[int], video_cap: cv2.VideoCapture = None, *_, **__
    ):
        raise ValueError("model-like classifier only support loading data from files")
