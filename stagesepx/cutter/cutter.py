import typing
import numpy as np
from loguru import logger

from stagesepx import toolbox
from stagesepx.cutter.cut_range import VideoCutRange
from stagesepx.cutter.cut_result import VideoCutResult
from stagesepx.video import VideoObject
from stagesepx.hook import BaseHook, GreyHook, CompressHook


class VideoCutter(object):
    def __init__(self,
                 step: int = None,
                 compress_rate: float = None,
                 target_size: typing.Tuple[int, int] = None,
                 ):
        """
        init video cutter

        :param step: step between frames, default to 1
        :param compress_rate:
        :param target_size:
        """
        if not step:
            step = 1
        self.step = step

        # default compress rate is 0.2
        if (not compress_rate) and (not target_size):
            logger.debug(f'no compress rate or target size received. set compress rate to 0.2')
            compress_rate = 0.2

        # init inner hook
        self._hook_list: typing.List[BaseHook] = list()
        compress_hook = CompressHook(overwrite=True, compress_rate=compress_rate, target_size=target_size)
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

    def _apply_hook(self, frame_id: int, frame: np.ndarray, *args, **kwargs) -> np.ndarray:
        for each_hook in self._hook_list:
            frame = each_hook.do(frame_id, frame, *args, **kwargs)
        return frame

    def _convert_video_into_range_list(self,
                                       video: VideoObject,
                                       block: int = None,
                                       *args,
                                       **kwargs) -> typing.List[VideoCutRange]:
        if not block:
            block = 2

        range_list: typing.List[VideoCutRange] = list()
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
            start = self._apply_hook(start_frame_id, start)

            # check block
            if not self.is_block_valid(start, block):
                logger.warning('array split does not result in an equal division, set block to 1')
                block = 1

            while ret:
                # hook
                end = self._apply_hook(end_frame_id, end, *args, **kwargs)

                logger.debug(f'computing {start_frame_id}({start_frame_time}) & {end_frame_id}({end_frame_time}) ...')
                start_part_list = self.pic_split(start, block)
                end_part_list = self.pic_split(end, block)

                # find the min ssim and the max mse / psnr
                ssim = 1.
                mse = 0.
                psnr = 0.
                for part_index, (each_start, each_end) in enumerate(zip(start_part_list, end_part_list)):
                    part_ssim = toolbox.compare_ssim(each_start, each_end)
                    if part_ssim < ssim:
                        ssim = part_ssim

                    # mse is very sensitive
                    part_mse = toolbox.calc_mse(each_start, each_end)
                    if part_mse > mse:
                        mse = part_mse

                    part_psnr = toolbox.calc_psnr(each_start, each_end)
                    if part_psnr > psnr:
                        psnr = part_psnr
                    logger.debug(f'part {part_index}: ssim={part_ssim}; mse={part_mse}; psnr={part_psnr}')
                logger.debug(f'between {start_frame_id} & {end_frame_id}: ssim={ssim}; mse={mse}; psnr={psnr}')

                range_list.append(
                    VideoCutRange(
                        video,
                        start=start_frame_id,
                        end=end_frame_id,
                        ssim=[ssim],
                        mse=[mse],
                        psnr=[psnr],
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

        return range_list

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
        # [Range(1-2), Range(2-3), Range(3-4) ... Range(99-100)]
        range_list = self._convert_video_into_range_list(
            video,
            *args,
            **kwargs)
        logger.info(f'cut finished: {video_path}')

        # TODO other analysis results can be added to VideoCutResult, such as AI cutter?
        return VideoCutResult(
            video,
            range_list,
        )
