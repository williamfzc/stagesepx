import typing
import time
import numpy as np
from loguru import logger

from stagesepx import toolbox
from stagesepx.cutter.cut_range import VideoCutRange
from stagesepx.cutter.cut_result import VideoCutResult
from stagesepx.video import VideoObject, VideoFrame
from stagesepx.hook import BaseHook, GreyHook, CompressHook


class VideoCutter(object):
    def __init__(
        self,
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
        self.step = step or 1

        # default compress rate is 0.2
        if (not compress_rate) and (not target_size):
            logger.debug(
                f"no compress rate or target size received. set compress rate to 0.2"
            )
            compress_rate = 0.2

        # init inner hook
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

    @staticmethod
    def pic_split(origin: np.ndarray, block: int) -> typing.List[np.ndarray]:
        """ actually, when block == 3, blocks' count would be 3 * 3 = 9 """
        result: typing.List[np.ndarray] = list()
        for each_block in np.array_split(origin, block, axis=0):
            sub_block = np.array_split(each_block, block, axis=1)
            result += sub_block
        return result

    def _apply_hook(self, frame: VideoFrame, *args, **kwargs) -> VideoFrame:
        for each_hook in self._hook_list:
            frame = each_hook.do(frame, *args, **kwargs)
        return frame

    def _convert_video_into_range_list(
        self, video: VideoObject, block: int = None, *args, **kwargs
    ) -> typing.List[VideoCutRange]:

        range_list: typing.List[VideoCutRange] = list()
        logger.info(f"total frame count: {video.frame_count}, size: {video.frame_size}")

        # load the first two frames
        video_operator = video.get_operator()
        cur_frame = video_operator.get_frame_by_id(1)
        next_frame = video_operator.get_frame_by_id(1 + self.step)

        # hook
        cur_frame = self._apply_hook(cur_frame)

        # check block
        if not block:
            block = 3

        while True:
            # hook
            next_frame = self._apply_hook(next_frame, *args, **kwargs)

            logger.debug(
                f"computing {cur_frame.frame_id}({cur_frame.timestamp}) & {next_frame.frame_id}({next_frame.timestamp}) ..."
            )
            start_part_list = self.pic_split(cur_frame.data, block)
            end_part_list = self.pic_split(next_frame.data, block)

            # find the min ssim and the max mse / psnr
            ssim = 1.0
            mse = 0.0
            psnr = 0.0
            for part_index, (each_start, each_end) in enumerate(
                zip(start_part_list, end_part_list)
            ):
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
                logger.debug(
                    f"part {part_index}: ssim={part_ssim}; mse={part_mse}; psnr={part_psnr}"
                )
            logger.debug(
                f"between {cur_frame.frame_id} & {next_frame.frame_id}: ssim={ssim}; mse={mse}; psnr={psnr}"
            )

            range_list.append(
                VideoCutRange(
                    video,
                    start=cur_frame.frame_id,
                    end=next_frame.frame_id,
                    ssim=[ssim],
                    mse=[mse],
                    psnr=[psnr],
                    start_time=cur_frame.timestamp,
                    end_time=next_frame.timestamp,
                )
            )

            # load the next one
            cur_frame = next_frame
            next_frame = video_operator.get_frame_by_id(next_frame.frame_id + self.step)
            if next_frame is None:
                break

        return range_list

    def cut(
        self, video: typing.Union[str, VideoObject], *args, **kwargs
    ) -> VideoCutResult:
        """
        convert video file, into a VideoCutResult

        :param video: video file path or VideoObject
        :param kwargs: parameters of toolbox.compress_frame can be used here
        :return:
        """
        start_time = time.time()
        if isinstance(video, str):
            video = VideoObject(video)

        logger.info(f"start cutting: {video.path}")

        # if video contains 100 frames
        # it starts from 1, and length of list is 99, not 100
        # [Range(1-2), Range(2-3), Range(3-4) ... Range(99-100)]
        range_list = self._convert_video_into_range_list(video, *args, **kwargs)
        logger.info(f"cut finished: {video}")
        end_time = time.time()
        logger.debug(f"cutter cost: {end_time - start_time}")

        # TODO other analysis results can be added to VideoCutResult, such as AI cutter?
        return VideoCutResult(video, range_list, cut_kwargs=kwargs)
