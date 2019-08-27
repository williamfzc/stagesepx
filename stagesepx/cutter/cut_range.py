import os
import typing
import random
import cv2
import numpy as np
from loguru import logger
from findit import FindIt

from stagesepx import toolbox
from stagesepx.video import VideoObject


class VideoCutRange(object):
    def __init__(self,
                 video: typing.Union[VideoObject, typing.Dict],
                 start: int,
                 end: int,

                 # TODO need refactored ?
                 ssim: typing.List[float],
                 mse: typing.List[float],
                 psnr: typing.List[float],

                 start_time: float,
                 end_time: float):
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

    def can_merge(self, another: 'VideoCutRange', offset: int = None, **_):
        if not offset:
            is_continuous = self.end == another.start
        else:
            is_continuous = self.end + offset >= another.start
        return is_continuous and self.video.path == another.video.path

    def merge(self, another: 'VideoCutRange', **kwargs) -> 'VideoCutRange':
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

    def contain_image(self,
                      image_path: str = None,
                      image_object: np.ndarray = None,
                      threshold: float = None,
                      *args, **kwargs):
        assert image_path or image_object, 'should fill image_path or image_object'
        if not threshold:
            threshold = 0.99

        if image_path:
            logger.debug(f'found image path, use it first: {image_path}')
            assert os.path.isfile(image_path), f'image {image_path} not existed'
            image_object = cv2.imread(image_path)
        image_object = toolbox.turn_grey(image_object)

        # TODO use client or itself..?
        fi = FindIt(
            engine=['template']
        )
        fi_template_name = 'default'
        fi.load_template(fi_template_name, pic_object=image_object)

        with toolbox.video_capture(self.video.path) as cap:
            target_id = self.pick(*args, **kwargs)[0]
            frame = toolbox.get_frame(cap, target_id)
            frame = toolbox.turn_grey(frame)

            result = fi.find(str(target_id), target_pic_object=frame)
        find_result = result['data'][fi_template_name]['TemplateEngine']
        position = find_result['target_point']
        sim = find_result['target_sim']
        logger.debug(f'position: {position}, sim: {sim}')
        return sim > threshold

    def pick(self,
             frame_count: int = None,
             is_random: bool = None,
             *_, **__) -> typing.List[int]:
        if not frame_count:
            frame_count = 3
        logger.debug(f'pick {frame_count} frames '
                     f'from {self.start}({self.start_time}) '
                     f'to {self.end}({self.end_time}) '
                     f'on video {self.video.path}')

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

    def get_frames(self,
                   frame_id_list: typing.List[int],
                   *_, **__) -> typing.List[toolbox.VideoFrame]:
        """ return a list of VideoFrame, usually works with pick """
        out = list()
        with toolbox.video_capture(self.video.path) as cap:
            for each_id in frame_id_list:
                timestamp = toolbox.get_frame_time(cap, each_id)
                frame = toolbox.get_frame(cap, each_id)
                out.append(toolbox.VideoFrame(each_id, timestamp, frame))
        return out

    def pick_and_get(self, *args, **kwargs) -> typing.List[toolbox.VideoFrame]:
        picked = self.pick(*args, **kwargs)
        return self.get_frames(picked, *args, **kwargs)

    def get_length(self):
        return self.end - self.start + 1

    def is_stable(self,
                  threshold: float = None,
                  psnr_threshold: float = None,
                  **_) -> bool:
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
        with toolbox.video_capture(video_path=self.video.path) as cap:
            start_frame = toolbox.get_frame(cap, self.start)
            end_frame = toolbox.get_frame(cap, self.end)
            start_frame, end_frame = map(toolbox.compress_frame, (start_frame, end_frame))
            return toolbox.compare_ssim(start_frame, end_frame) > threshold

    def diff(self, another: 'VideoCutRange', *args, **kwargs) -> typing.List[float]:
        self_picked = self.pick_and_get(*args, **kwargs)
        another_picked = another.pick_and_get(*args, **kwargs)
        return toolbox.multi_compare_ssim(self_picked, another_picked)

    def __str__(self):
        return f'<VideoCutRange [{self.start}({self.start_time})-{self.end}({self.end_time})] ssim={self.ssim}>'

    __repr__ = __str__
