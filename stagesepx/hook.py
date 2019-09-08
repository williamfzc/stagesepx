import numpy as np
import os
from loguru import logger
import cv2
import typing
from findit import FindIt

from stagesepx import toolbox


class BaseHook(object):
    def __init__(self, overwrite: bool = None, *_, **__):
        logger.debug(f'start initialing: {self.__class__.__name__} ...')

        # default: dict
        self.result = dict()

        # overwrite label
        # decide whether the origin frame will be changed
        self.overwrite = bool(overwrite)
        logger.debug(f'overwrite: {self.overwrite}')

    def do(self, frame_id: int, frame: np.ndarray, *_, **__) -> typing.Optional[np.ndarray]:
        info = f'execute hook: {self.__class__.__name__}'

        # when frame id == -1, it means handling some pictures outside the video
        if frame_id != -1:
            logger.debug(f'{info}, frame id: {frame_id}')
        return


def change_origin(_func):
    def _wrap(self: BaseHook, frame_id: int, frame: np.ndarray, *args, **kwargs):
        res = _func(self, frame_id, frame, *args, **kwargs)
        if not self.overwrite:
            return frame
        if res is not None:
            logger.debug(f'origin frame has been changed by {self.__class__.__name__}')
            return res
        else:
            return frame

    return _wrap


class ExampleHook(BaseHook):
    """ this hook will help you write your own hook class """

    def __init__(self, *_, **__):
        """
        hook has two ways to affect the result of analysis

        1. add your result to self.result (or somewhere else), and get it by yourself after cut or classify
        2. use label 'overwrite'. by enabling this, hook will changing the origin frame
        """
        super().__init__(*_, **__)

        # add your code here
        # ...

    @change_origin
    def do(self, frame_id: int, frame: np.ndarray, *_, **__) -> typing.Optional[np.ndarray]:
        super().do(frame_id, frame, *_, **__)

        # you can get frame_id and frame data here
        # and use them to custom your own function

        # add your code here
        # ...

        # for example, i want to turn grey, and save size of each frames
        frame = toolbox.turn_grey(frame)
        self.result[frame_id] = frame.shape

        # if you are going to change the origin frame
        # just return the changed frame
        # and set 'overwrite' to 'True' when you are calling __init__
        return frame

        # for safety, if you do not want to modify the origin frame
        # you can return a 'None' instead of frame
        # and nothing will happen even if setting 'overwrite' to 'True'


# --- inner hook start ---

class CompressHook(BaseHook):
    def __init__(self, compress_rate: float, target_size: typing.Tuple[int, int], *_, **__):
        super().__init__(*_, **__)
        self.compress_rate = compress_rate
        self.target_size = target_size
        logger.debug(f'compress rate: {compress_rate}')
        logger.debug(f'target size: {target_size}')

    @change_origin
    def do(self, frame_id: int, frame: np.ndarray, *_, **__) -> typing.Optional[np.ndarray]:
        super().do(frame_id, frame, *_, **__)
        return toolbox.compress_frame(frame, compress_rate=self.compress_rate, target_size=self.target_size)


class GreyHook(BaseHook):
    @change_origin
    def do(self, frame_id: int, frame: np.ndarray, *_, **__) -> typing.Optional[np.ndarray]:
        super().do(frame_id, frame, *_, **__)
        return toolbox.turn_grey(frame)


class RefineHook(BaseHook):
    """ this hook was built for refining the edges of images """

    @change_origin
    def do(self, frame_id: int, frame: np.ndarray, *_, **__) -> typing.Optional[np.ndarray]:
        super().do(frame_id, frame, *_, **__)
        return toolbox.sharpen_frame(frame)


class CropHook(BaseHook):
    """ this hook was built for cropping frames, eg: keep only a half of origin frame """

    def __init__(self,
                 size: typing.Tuple[typing.Union[int, float], typing.Union[int, float]],
                 offset: typing.Tuple[typing.Union[int, float], typing.Union[int, float]] = None,
                 *_, **__):
        """
        init crop hook, (height, width)

        :param size:
        :param offset:
        :param _:
        :param __:
        """
        super().__init__(*_, **__)

        self.size = size
        self.offset = offset or (0, 0)
        logger.debug(f'size: {self.size}')
        logger.debug(f'offset: {self.offset}')

    @staticmethod
    def is_proportion(target: typing.Tuple[typing.Union[int, float], typing.Union[int, float]]) -> bool:
        return len([i for i in target if 0. <= i <= 1.]) == 2

    @change_origin
    def do(self, frame_id: int, frame: np.ndarray, *_, **__) -> typing.Optional[np.ndarray]:
        super().do(frame_id, frame, *_, **__)
        origin_h, origin_w = frame.shape
        logger.debug(f'origin size: ({origin_h}, {origin_w})')

        # convert to real size
        size_h, size_w = self.size
        if self.is_proportion(self.size):
            size_h, size_w = origin_h * self.size[0], origin_w * self.size[1]
        logger.debug(f'size: ({size_h}, {size_w})')

        offset_h, offset_w = self.offset
        if self.is_proportion(self.offset):
            offset_h, offset_w = origin_h * self.offset[0], origin_w * self.offset[1]
        logger.debug(f'offset: {offset_h}, {offset_w}')

        height_range = (int(offset_h), int(offset_h + size_h))
        width_range = (int(offset_w), int(offset_w + size_w))
        logger.debug(f'crop range h: {height_range}, w: {width_range}')
        return frame[height_range[0]: height_range[1], width_range[0]: width_range[1]]


# --- inner hook end ---

class FrameSaveHook(BaseHook):
    """ add this hook, and save all the frames you want to specific dir """

    def __init__(self, target_dir: str, *_, **__):
        super().__init__(*_, **__)

        # init target dir
        self.target_dir = target_dir
        os.makedirs(target_dir, exist_ok=True)

        logger.debug(f'target dir: {target_dir}')

    @change_origin
    def do(self,
           frame_id: int,
           frame: np.ndarray,
           *_, **__) -> typing.Optional[np.ndarray]:
        super().do(frame_id, frame, *_, **__)
        target_path = os.path.join(self.target_dir, f'{frame_id}.png')
        cv2.imwrite(target_path, frame)
        logger.debug(f'frame saved to {target_path}')
        return


class InvalidFrameDetectHook(BaseHook):
    def __init__(self,
                 black_threshold: float = None,
                 white_threshold: float = None,
                 *_, **__):
        super().__init__(*_, **__)

        # threshold
        self.black_threshold = black_threshold or 0.95
        self.white_threshold = white_threshold or 0.9

        logger.debug(f'black threshold: {black_threshold}')
        logger.debug(f'white threshold: {white_threshold}')

    @change_origin
    def do(self,
           frame_id: int,
           frame: np.ndarray,
           *_, **__) -> typing.Optional[np.ndarray]:
        super().do(frame_id, frame, *_, **__)
        black = np.zeros([*frame.shape, 3], np.uint8)
        white = black + 255
        black_ssim = toolbox.compare_ssim(black, frame)
        white_ssim = toolbox.compare_ssim(white, frame)
        logger.debug(f'black: {black_ssim}; white: {white_ssim}')

        self.result[frame_id] = {
            'black': black_ssim,
            'white': white_ssim,
        }
        return


class TemplateCompareHook(BaseHook):
    def __init__(self,
                 template_dict: typing.Dict[str, str],
                 *args, **kwargs):
        """
        args and kwargs will be sent to findit.__init__

        :param template_dict:
            # k: template name
            # v: template picture path
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.fi = FindIt(*args, **kwargs)
        self.template_dict = template_dict

    @change_origin
    def do(self,
           frame_id: int,
           frame: np.ndarray,
           *_, **__) -> typing.Optional[np.ndarray]:
        super().do(frame_id, frame, *_, **__)
        for each_template_name, each_template_path in self.template_dict.items():
            self.fi.load_template(each_template_name, each_template_path)
        res = self.fi.find(str(frame_id), target_pic_object=frame)
        logger.debug(f'compare with template {self.template_dict}: {res}')
        self.result[frame_id] = res
        return


class BinaryHook(BaseHook):
    @change_origin
    def do(self, frame_id: int, frame: np.ndarray, *_, **__) -> typing.Optional[np.ndarray]:
        # TODO not always work
        super().do(frame_id, frame, *_, **__)
        return toolbox.turn_binary(frame)
