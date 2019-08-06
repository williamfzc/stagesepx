import os
import typing
import numpy as np
from loguru import logger

from stagesepx import toolbox
from stagesepx.cutter.cut_range import VideoCutRange
from stagesepx.cutter.cut_result import VideoCutResult


class VideoCutter(object):
    def __init__(self,
                 step: int = None,
                 # TODO removed in the future
                 compress_rate: float = None):
        """
        init video cutter

        :param step: step between frames, default to 1
        :param compress_rate: (moved to `cut`) before * compress_rate = after
        """
        if not step:
            step = 1
        self.step = step

        if compress_rate:
            logger.warning('compress_rate has been moved to func `cut`')

    @staticmethod
    def pic_split(origin: np.ndarray, column: int) -> typing.List[np.ndarray]:
        res = [
            np.hsplit(np.vsplit(origin, column)[i], column)
            for i in range(column)
        ]
        return [j for i in res for j in i]

    def convert_video_into_ssim_list(self, video_path: str, block: int = None, **kwargs) -> typing.List[VideoCutRange]:
        if not block:
            block = 2

        ssim_list = list()
        with toolbox.video_capture(video_path) as cap:
            # get video info
            frame_count = toolbox.get_frame_count(cap)
            frame_size = toolbox.get_frame_size(cap)
            logger.debug(f'total frame count: {frame_count}, size: {frame_size}')

            # load the first two frames
            _, start = cap.read()
            start_frame_id = toolbox.get_current_frame_id(cap)
            start_frame_time = toolbox.get_current_frame_time(cap)

            toolbox.video_jump(cap, self.step + 1)
            ret, end = cap.read()
            end_frame_id = toolbox.get_current_frame_id(cap)
            end_frame_time = toolbox.get_current_frame_time(cap)

            # compress
            start = toolbox.compress_frame(start, **kwargs)

            while ret:
                end = toolbox.compress_frame(end, **kwargs)

                start_part_list = self.pic_split(start, block)
                end_part_list = self.pic_split(end, block)

                ssim = 1.
                for part_index, (each_start, each_end) in enumerate(zip(start_part_list, end_part_list)):
                    part_ssim = toolbox.compare_ssim(each_start, each_end)
                    if part_ssim < ssim:
                        ssim = part_ssim
                    logger.debug(f'part {part_index}: {part_ssim}')
                logger.debug(f'ssim between {start_frame_id} & {end_frame_id}: {ssim}')

                ssim_list.append(
                    VideoCutRange(
                        video_path,
                        start=start_frame_id,
                        end=end_frame_id,
                        ssim=[ssim],
                        start_time=start_frame_time,
                        end_time=end_frame_time,
                    )
                )

                # load the next one
                start = end
                start_frame_id, end_frame_id = end_frame_id, end_frame_id + self.step
                start_frame_time = end_frame_time
                toolbox.video_jump(cap, end_frame_id)
                ret, end = cap.read()
                end_frame_time = toolbox.get_current_frame_time(cap)

        return ssim_list

    def cut(self, video_path: str, **kwargs) -> VideoCutResult:
        """
        convert video file, into a VideoCutResult

        :param video_path: video file path
        :param kwargs: parameters of toolbox.compress_frame can be used here
        :return:
        """

        logger.info(f'start cutting: {video_path}')
        assert os.path.isfile(video_path), f'video [{video_path}] not existed'

        # if video contains 100 frames
        # it starts from 1, and length of list is 99, not 100
        # [SSIM(1-2), SSIM(2-3), SSIM(3-4) ... SSIM(99-100)]
        ssim_list = self.convert_video_into_ssim_list(video_path, **kwargs)
        logger.info(f'cut finished: {video_path}')

        # TODO other analysis results can be added to VideoCutResult, such as AI cutter?
        return VideoCutResult(
            video_path,
            ssim_list,
        )
