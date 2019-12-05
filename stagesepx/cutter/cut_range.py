import os
import typing
import random
import numpy as np
from loguru import logger
from findit import FindIt

from stagesepx import toolbox
from stagesepx.video import VideoObject, VideoFrame


class VideoCutRange(object):
    def __init__(
        self,
        # TODO why can it be a dict?
        video: typing.Union[VideoObject, typing.Dict],
        start: int,
        end: int,
        # TODO need refactored ?
        ssim: typing.List[float],
        mse: typing.List[float],
        psnr: typing.List[float],
        start_time: float,
        end_time: float,
    ):
        if isinstance(video, dict):
            self.video = VideoObject(**video)
        else:
            self.video = video

        self.start = start
        self.end = end
        self.ssim = ssim
        self.mse = mse
        self.psnr = psnr
        self.start_time = start_time
        self.end_time = end_time

        # if length is 1
        # https://github.com/williamfzc/stagesepx/issues/9
        if start > end:
            self.start, self.end = self.end, self.start
            self.start_time, self.end_time = self.end_time, self.start_time

        logger.debug(
            f"new a range: {self.start}({self.start_time}) - {self.end}({self.end_time})"
        )

    def can_merge(self, another: "VideoCutRange", offset: int = None, **_):
        if not offset:
            is_continuous = self.end == another.start
        else:
            is_continuous = self.end + offset >= another.start
        return is_continuous and self.video.path == another.video.path

    def merge(self, another: "VideoCutRange", **kwargs) -> "VideoCutRange":
        assert self.can_merge(another, **kwargs)
        return __class__(
            self.video,
            self.start,
            another.end,
            self.ssim + another.ssim,
            self.mse + another.mse,
            self.psnr + another.psnr,
            self.start_time,
            another.end_time,
        )

    def contain(self, frame_id: int) -> bool:
        # in python:
        # range(0, 10) => [0, 10)
        # range(0, 10 + 1) => [0, 10]
        return frame_id in range(self.start, self.end + 1)

    # alias
    contain_frame_id = contain

    def contain_image(
        self, image_path: str = None, image_object: np.ndarray = None, *args, **kwargs
    ) -> typing.Dict[str, typing.Any]:
        # todo pick only one picture?
        target_id = self.pick(*args, **kwargs)[0]
        operator = self.video.get_operator()
        frame = operator.get_frame_by_id(target_id)
        return frame.contain_image(
            image_path=image_path, image_object=image_object, **kwargs
        )

    def pick(
        self, frame_count: int = None, is_random: bool = None, *_, **__
    ) -> typing.List[int]:
        if not frame_count:
            frame_count = 3
        logger.debug(
            f"pick {frame_count} frames "
            f"from {self.start}({self.start_time}) "
            f"to {self.end}({self.end_time}) "
            f"on video {self.video.path}"
        )

        result = list()
        if is_random:
            return random.sample(range(self.start, self.end), frame_count)
        length = self.get_length()

        # https://github.com/williamfzc/stagesepx/issues/37
        frame_count += 1
        for _ in range(1, frame_count):
            cur = int(self.start + length / frame_count * _)
            result.append(cur)
        return result

    def get_frames(
        self, frame_id_list: typing.List[int], *_, **__
    ) -> typing.List[VideoFrame]:
        """ return a list of VideoFrame, usually works with pick """
        out = list()
        operator = self.video.get_operator()
        for each_id in frame_id_list:
            frame = operator.get_frame_by_id(each_id)
            out.append(frame)
        return out

    def pick_and_get(self, *args, **kwargs) -> typing.List[VideoFrame]:
        picked = self.pick(*args, **kwargs)
        return self.get_frames(picked, *args, **kwargs)

    def get_length(self):
        return self.end - self.start + 1

    def is_stable(
        self, threshold: float = None, psnr_threshold: float = None, **_
    ) -> bool:
        # IMPORTANT function!
        # it decided whether a range is stable => everything is based on it!
        if not threshold:
            threshold = 0.95

        # ssim
        res = np.mean(self.ssim) > threshold
        # psnr (double check if stable)
        if res and psnr_threshold:
            res = np.mean(self.psnr) > psnr_threshold

        return res

    def is_loop(self, threshold: float = None, **_) -> bool:
        if not threshold:
            threshold = 0.95
        operator = self.video.get_operator()
        start_frame = operator.get_frame_by_id(self.start)
        end_frame = operator.get_frame_by_id(self.end)
        return toolbox.compare_ssim(start_frame.data, end_frame.data) > threshold

    def diff(self, another: "VideoCutRange", *args, **kwargs) -> typing.List[float]:
        self_picked = self.pick_and_get(*args, **kwargs)
        another_picked = another.pick_and_get(*args, **kwargs)
        return toolbox.multi_compare_ssim(self_picked, another_picked)

    def __str__(self):
        return f"<VideoCutRange [{self.start}({self.start_time})-{self.end}({self.end_time})] ssim={self.ssim}>"

    __repr__ = __str__
