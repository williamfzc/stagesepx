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
                 video: VideoObject,
                 start: int,
                 end: int,
                 ssim: typing.List,
                 start_time: float,
                 end_time: float):
        self.video = video
        self.start = start
        self.end = end
        self.ssim = ssim
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
            frame_count = 1

        result = list()
        if is_random:
            return random.sample(range(self.start, self.end), frame_count)
        length = self.get_length()
        for _ in range(frame_count):
            cur = int(self.start + length / frame_count * _)
            result.append(cur)
        return result

    def get_length(self):
        return self.end - self.start + 1

    def is_stable(self, threshold: float = None, **_) -> bool:
        if not threshold:
            threshold = 0.95
        return np.mean(self.ssim) > threshold

    def is_loop(self, threshold: float = None, **_) -> bool:
        if not threshold:
            threshold = 0.95
        with toolbox.video_capture(video_path=self.video.path) as cap:
            start_frame = toolbox.get_frame(cap, self.start)
            end_frame = toolbox.get_frame(cap, self.end)
            start_frame, end_frame = map(toolbox.compress_frame, (start_frame, end_frame))
            return toolbox.compare_ssim(start_frame, end_frame) > threshold

    def __str__(self):
        return f'<VideoCutRange [{self.start}-{self.end}] ssim={self.ssim}>'

    __repr__ = __str__
