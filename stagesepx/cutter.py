import os
import typing
import random
import numpy as np
from loguru import logger

from stagesepx import toolbox


class VideoCutRange(object):
    def __init__(self, start: int, end: int, ssim: float):
        self.start = start
        self.end = end
        self.ssim = ssim

    def can_merge(self, another: 'VideoCutRange'):
        return self.end == another.start

    def merge(self, another: 'VideoCutRange') -> 'VideoCutRange':
        assert self.can_merge(another)
        return __class__(
            self.start,
            another.end,
            (self.ssim + another.ssim) / 2,
        )

    def pick(self, frame_count: int, is_random: bool = None):
        result = list()
        if is_random:
            return random.sample(range(self.start, self.end), frame_count)
        length = self.end - self.start
        for _ in range(1, frame_count):
            cur = int(self.start + length / frame_count * _)
            result.append(cur)
        return result

    def __str__(self):
        return f'<VideoCutRange [{self.start}-{self.end}] {self.ssim}>'


class VideoCutResult(object):
    def __init__(self,
                 video_path: str,
                 ssim_list: typing.List[VideoCutRange]):
        self.video_path = video_path
        self.ssim_list = ssim_list

    def get_unstable_range(self) -> typing.List[VideoCutRange]:
        middle = np.mean([i.ssim for i in self.ssim_list])
        change_range_list = sorted([i for i in self.ssim_list if i.ssim < middle], key=lambda x: x.start)

        # merge
        i = 0
        merged_change_range_list = list()
        while i < len(change_range_list) - 1:
            cur = change_range_list[i]
            while cur.can_merge(change_range_list[i + 1]):
                # can be merged
                i += 1
                cur = cur.merge(change_range_list[i])

                # out of range
                if i + 1 >= len(change_range_list):
                    break
            merged_change_range_list.append(cur)
            i += 1
        return merged_change_range_list

    def get_stable_range(self) -> typing.List[VideoCutRange]:
        total_range = [self.ssim_list[0].start, self.ssim_list[-1].end]
        unstable_range_list = self.get_unstable_range()
        range_list = [
            VideoCutRange(total_range[0], unstable_range_list[0].start, 0),
            VideoCutRange(unstable_range_list[-1].end, total_range[-1], 0),
        ]
        for i in range(len(unstable_range_list) - 1):
            range_list.append(
                VideoCutRange(
                    unstable_range_list[i].end,
                    unstable_range_list[i + 1].start,
                    0,
                )
            )
        return sorted(range_list, key=lambda x: x.start)


class VideoCutter(object):
    def __init__(self, period: int = None, compress_rate: float = None):
        if not period:
            period = 5
        if not compress_rate:
            compress_rate = 0.2

        self.period = period
        self.compress_rate = compress_rate

    def convert_video_into_ssim_list(self, video_path: str) -> typing.List[VideoCutRange]:
        ssim_list = list()
        with toolbox.video_capture(video_path) as cap:
            # load the first two frames
            _, start = cap.read()
            start_frame_id = toolbox.get_current_frame_id(cap)

            toolbox.video_jump(cap, self.period)
            ret, end = cap.read()
            end_frame_id = toolbox.get_current_frame_id(cap)

            # compress
            start = toolbox.compress_frame(start, compress_rate=self.compress_rate)

            while ret:
                end = toolbox.compress_frame(end, compress_rate=self.compress_rate)
                ssim = toolbox.compare_ssim(start, end)
                logger.debug(f'ssim between {start_frame_id} & {end_frame_id}: {ssim}')

                ssim_list.append(
                    VideoCutRange(
                        start=start_frame_id,
                        end=end_frame_id,
                        ssim=ssim,
                    )
                )

                # load the next one
                start = end
                start_frame_id, end_frame_id = end_frame_id, end_frame_id + self.period
                toolbox.video_jump(cap, end_frame_id)
                ret, end = cap.read()

        return ssim_list

    def cut(self, video_path: str) -> VideoCutResult:
        assert os.path.isfile(video_path), f'video [{video_path}] not existed'
        ssim_list = self.convert_video_into_ssim_list(video_path)
        return VideoCutResult(
            video_path,
            ssim_list,
        )
