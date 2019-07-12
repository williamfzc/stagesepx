import os
import typing
import cv2
import numpy as np
from loguru import logger

from stagesepx import toolbox


class VideoCutResult(object):
    pass


class VideoCutter(object):
    class _Range(object):
        def __init__(self, start: int, end: int, ssim: float):
            self.start = start
            self.end = end
            self.ssim = ssim

        def can_merge(self, another: '_Range'):
            return self.end == another.start

        def merge(self, another: '_Range') -> '_Range':
            assert self.can_merge(another)
            return __class__(
                self.start,
                another.end,
                (self.ssim + another.ssim) / 2,
            )

        def __str__(self):
            return f'<Range [{self.start}-{self.end}] {self.ssim}>'

    def __init__(self, period: int = None, compress_rate: float = None):
        if not period:
            period = 5
        if not compress_rate:
            compress_rate = 0.2

        self.period = period
        self.compress_rate = compress_rate

    def convert_video_into_ssim_list(self, video_path: str) -> typing.List[_Range]:
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
                    self._Range(
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

    def get_unstable_range(self, ssim_list: typing.List[_Range]) -> typing.List[_Range]:
        middle = np.mean([i.ssim for i in ssim_list])
        change_range_list = sorted([i for i in ssim_list if i.ssim < middle], key=lambda x: x.start)

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

    def get_stable_range(self, ssim_list: typing.List[_Range]) -> typing.List[_Range]:
        total_range = [ssim_list[0].start, ssim_list[-1].end]
        unstable_range_list = self.get_unstable_range(ssim_list)
        range_list = [
            self._Range(total_range[0], unstable_range_list[0].start, 0),
            self._Range(unstable_range_list[-1].end, total_range[-1], 0),
        ]
        for i in range(len(unstable_range_list) - 1):
            range_list.append(
                self._Range(
                    unstable_range_list[i].end,
                    unstable_range_list[i + 1].start,
                    0,
                )
            )
        return sorted(range_list, key=lambda x: x.start)

    def cut(self, video_path: str) -> VideoCutResult:
        assert os.path.isfile(video_path), f'video [{video_path}] not existed'
        ssim_list = self.convert_video_into_ssim_list(video_path)
        print(ssim_list)
