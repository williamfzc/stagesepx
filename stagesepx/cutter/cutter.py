import typing
import numpy as np
from loguru import logger

from stagesepx import toolbox
from stagesepx.cutter.cut_range import VideoCutRange
from stagesepx.cutter.cut_result import VideoCutResult
from stagesepx.video import VideoObject
from stagesepx.hook import BaseHook


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

        self._hook_list: typing.List[BaseHook] = list()

    def add_hook(self, new_hook: BaseHook):
        """
        add a hook

        :param new_hook:
        :return:
        """
        self._hook_list.append(new_hook)
        logger.debug(f'add hook: {new_hook.__class__.__name__}')

    @staticmethod
    def pic_split(origin: np.ndarray, block: int) -> typing.List[np.ndarray]:
        res = [
            np.hsplit(np.vsplit(origin, block)[i], block)
            for i in range(block)
        ]
        return [j for i in res for j in i]

    @staticmethod
    def is_block_valid(origin: np.ndarray, block: int) -> bool:
        try:
            _ = [
                np.hsplit(np.vsplit(origin, block)[i], block)
                for i in range(block)
            ]
        except ValueError:
            return False
        else:
            return True

    def _apply_hook(self, frame_id: int, frame: np.ndarray, *args, **kwargs):
        for each_hook in self._hook_list:
            each_hook.do(frame_id, frame, *args, **kwargs)

    def _convert_video_into_ssim_list(self,
                                      video: VideoObject,
                                      block: int = None,
                                      *args,
                                      **kwargs) -> typing.List[VideoCutRange]:
        if not block:
            block = 2

        ssim_list = list()
        with toolbox.video_capture(video.path) as cap:
            logger.debug(f'total frame count: {video.frame_count}, size: {video.frame_size}')

            # load the first two frames
            _, start = cap.read()
            start_frame_id = toolbox.get_current_frame_id(cap)
            start_frame_time = toolbox.get_current_frame_time(cap)

            toolbox.video_jump(cap, self.step + 1)
            ret, end = cap.read()
            end_frame_id = toolbox.get_current_frame_id(cap)
            end_frame_time = toolbox.get_current_frame_time(cap)

            # hook
            self._apply_hook(start_frame_id, start)

            # compress
            start = toolbox.compress_frame(start, **kwargs)

            # check block
            if not self.is_block_valid(start, block):
                logger.warning('array split does not result in an equal division, set block to 1')
                block = 1

            while ret:
                # hook
                self._apply_hook(end_frame_id, end, *args, **kwargs)

                end = toolbox.compress_frame(end, **kwargs)
                logger.debug(f'computing {start_frame_id} & {end_frame_id} ...')
                start_part_list = self.pic_split(start, block)
                end_part_list = self.pic_split(end, block)

                # find the min ssim
                ssim = 1.
                for part_index, (each_start, each_end) in enumerate(zip(start_part_list, end_part_list)):
                    part_ssim = toolbox.compare_ssim(each_start, each_end)
                    if part_ssim < ssim:
                        ssim = part_ssim
                    logger.debug(f'part {part_index}: {part_ssim}')
                logger.debug(f'ssim between {start_frame_id} & {end_frame_id}: {ssim}')

                ssim_list.append(
                    VideoCutRange(
                        video,
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

    def cut(self, video_path: str, *args, **kwargs) -> VideoCutResult:
        """
        convert video file, into a VideoCutResult

        :param video_path: video file path
        :param kwargs: parameters of toolbox.compress_frame can be used here
        :return:
        """

        logger.info(f'start cutting: {video_path}')
        video = VideoObject(video_path)

        # if video contains 100 frames
        # it starts from 1, and length of list is 99, not 100
        # [SSIM(1-2), SSIM(2-3), SSIM(3-4) ... SSIM(99-100)]
        ssim_list = self._convert_video_into_ssim_list(
            video,
            *args,
            **kwargs)
        logger.info(f'cut finished: {video_path}')

        # TODO other analysis results can be added to VideoCutResult, such as AI cutter?
        return VideoCutResult(
            video,
            ssim_list,
        )
