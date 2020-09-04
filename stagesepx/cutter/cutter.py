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

    def compare_frame_list(
        self, src: typing.List[np.ndarray], target: typing.List[np.ndarray]
    ) -> typing.List[float]:
        """
        core method about how to compare two lists of ndarray and get their ssim/mse/psnr
        you can overwrite this method to implement your own algo
        see https://github.com/williamfzc/stagesepx/issues/136

        :param src:
        :param target:
        :return:
        """
        # find the min ssim and the max mse / psnr
        ssim = 1.0
        mse = 0.0
        psnr = 0.0

        for part_index, (each_start, each_end) in enumerate(zip(src, target)):
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
        return [ssim, mse, psnr]

    def _convert_video_into_range_list(
        self, video: VideoObject, block: int, window_size: int, window_coefficient: int
    ) -> typing.List[VideoCutRange]:

        step = self.step
        video_length = video.frame_count

        class _Window(object):
            def __init__(self):
                self.start = 1
                self.size = window_size
                self.end = self.start + window_size * step

            def load_data(self) -> typing.List[VideoFrame]:
                cur = self.start
                result = []
                video_operator = video.get_operator()
                while cur <= self.end:
                    frame = video_operator.get_frame_by_id(cur)
                    result.append(frame)
                    cur += step
                # at least 2
                if len(result) < 2:
                    last = video_operator.get_frame_by_id(self.end)
                    result.append(last)
                return result

            def shift(self) -> bool:
                logger.debug(f"window before: {self.start}, {self.end}")
                self.start += step
                self.end += step
                if self.start >= video_length:
                    # out of range
                    return False
                # window end
                if self.end >= video_length:
                    self.end = video_length
                logger.debug(f"window after: {self.start}, {self.end}")
                return True

        def _float_merge(float_list: typing.List[float]) -> float:
            # the first, the largest.
            length = len(float_list)
            result = 0.0
            denominator = 0.0
            for i, each in enumerate(float_list):
                weight = pow(length - i, window_coefficient)
                denominator += weight
                result += each * weight
                logger.debug(f"calc: {each} x {weight}")
            final = result / denominator
            logger.debug(f"calc final: {final} from {result} / {denominator}")
            return final

        range_list: typing.List[VideoCutRange] = list()
        logger.info(f"total frame count: {video_length}, size: {video.frame_size}")

        window = _Window()
        while True:
            frame_list = window.load_data()
            frame_list = [self._apply_hook(each) for each in frame_list]

            # window loop
            ssim_list = []
            mse_list = []
            psnr_list = []

            cur_frame = frame_list[0]
            first_target_frame = frame_list[1]
            cur_frame_list = self.pic_split(cur_frame.data, block)
            for each in frame_list[1:]:
                each_frame_list = self.pic_split(each.data, block)
                ssim, mse, psnr = self.compare_frame_list(
                    cur_frame_list, each_frame_list
                )
                ssim_list.append(ssim)
                mse_list.append(mse)
                psnr_list.append(psnr)
                logger.debug(
                    f"between {cur_frame.frame_id} & {each.frame_id}: ssim={ssim}; mse={mse}; psnr={psnr}"
                )
            ssim = _float_merge(ssim_list)
            mse = _float_merge(mse_list)
            psnr = _float_merge(psnr_list)

            range_list.append(
                VideoCutRange(
                    video,
                    start=cur_frame.frame_id,
                    end=first_target_frame.frame_id,
                    ssim=[ssim],
                    mse=[mse],
                    psnr=[psnr],
                    start_time=cur_frame.timestamp,
                    end_time=first_target_frame.timestamp,
                )
            )
            continue_flag = window.shift()
            if not continue_flag:
                break

        return range_list

    def cut(
        self,
        video: typing.Union[str, VideoObject],
        block: int = None,
        window_size: int = None,
        window_coefficient: int = None,
        *_,
        **kwargs,
    ) -> VideoCutResult:
        """
        convert video file, into a VideoCutResult

        :param video: video file path or VideoObject
        :param block: default to 3. when block == 3, frame will be split into 3 * 3 = 9 parts
        :param window_size:
        :param window_coefficient:
        :return:
        """
        # args
        if not block:
            block = 3
        if not window_size:
            window_size = 1
        if not window_coefficient:
            window_coefficient = 2

        start_time = time.time()
        if isinstance(video, str):
            video = VideoObject(video)

        logger.info(f"start cutting: {video.path}")

        # if video contains 100 frames
        # it starts from 1, and length of list is 99, not 100
        # [Range(1-2), Range(2-3), Range(3-4) ... Range(99-100)]
        range_list = self._convert_video_into_range_list(
            video, block, window_size, window_coefficient
        )
        logger.info(f"cut finished: {video}")
        end_time = time.time()
        logger.debug(f"cutter cost: {end_time - start_time}")

        # TODO other analysis results can be added to VideoCutResult, such as AI cutter?
        return VideoCutResult(video, range_list, cut_kwargs=kwargs)
