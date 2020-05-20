import os
from loguru import logger
import cv2
import typing
from findit import FindIt

from stagesepx import toolbox
from stagesepx.video import VideoFrame


class BaseHook(object):
    def __init__(self, *_, **__):
        logger.debug(f"start initialing: {self.__class__.__name__} ...")

        # default: dict
        self.result = dict()

    def do(self, frame: VideoFrame, *_, **__) -> typing.Optional[VideoFrame]:
        info = f"execute hook: {self.__class__.__name__}"

        frame_id = frame.frame_id
        # when frame id == -1, it means handling some pictures outside the video
        if frame_id != -1:
            logger.debug(f"{info}, frame id: {frame_id}")
        return frame


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

    def do(self, frame: VideoFrame, *_, **__) -> typing.Optional[VideoFrame]:
        super().do(frame, *_, **__)

        # you can get frame_id and frame data here
        # and use them to custom your own function

        # add your code here
        # ...

        # for example, i want to turn grey, and save size of each frames
        frame.data = toolbox.turn_grey(frame.data)
        self.result[frame.frame_id] = frame.data.shape

        # if you are going to change the origin frame
        # just return the changed frame
        # and set 'overwrite' to 'True' when you are calling __init__
        return frame

        # for safety, if you do not want to modify the origin frame
        # you can return a 'None' instead of frame
        # and nothing will happen even if setting 'overwrite' to 'True'


# --- inner hook start ---


class CompressHook(BaseHook):
    def __init__(
        self,
        compress_rate: float = None,
        target_size: typing.Tuple[int, int] = None,
        *_,
        **__,
    ):
        super().__init__(*_, **__)
        self.compress_rate = compress_rate
        self.target_size = target_size
        logger.debug(f"compress rate: {compress_rate}")
        logger.debug(f"target size: {target_size}")

    def do(self, frame: VideoFrame, *_, **__) -> typing.Optional[VideoFrame]:
        super().do(frame, *_, **__)
        frame.data = toolbox.compress_frame(
            frame.data, compress_rate=self.compress_rate, target_size=self.target_size
        )
        return frame


class GreyHook(BaseHook):
    def do(self, frame: VideoFrame, *_, **__) -> typing.Optional[VideoFrame]:
        super().do(frame, *_, **__)
        frame.data = toolbox.turn_grey(frame.data)
        return frame


class RefineHook(BaseHook):
    """ this hook was built for refining the edges of images """

    def do(self, frame: VideoFrame, *_, **__) -> typing.Optional[VideoFrame]:
        super().do(frame, *_, **__)
        frame.data = toolbox.sharpen_frame(frame.data)
        return frame


class _AreaBaseHook(BaseHook):
    def __init__(
        self,
        size: typing.Tuple[typing.Union[int, float], typing.Union[int, float]],
        offset: typing.Tuple[typing.Union[int, float], typing.Union[int, float]] = None,
        *_,
        **__,
    ):
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
        logger.debug(f"size: {self.size}")
        logger.debug(f"offset: {self.offset}")

    @staticmethod
    def is_proportion(
        target: typing.Tuple[typing.Union[int, float], typing.Union[int, float]]
    ) -> bool:
        return len([i for i in target if 0.0 <= i <= 1.0]) == 2

    @staticmethod
    def convert(
        origin_h: int,
        origin_w: int,
        input_h: typing.Union[float, int],
        input_w: typing.Union[float, int],
    ) -> typing.Tuple[typing.Union[int, float], typing.Union[int, float]]:
        if _AreaBaseHook.is_proportion((input_h, input_w)):
            return origin_h * input_h, origin_w * input_w
        return input_h, input_w

    def convert_size_and_offset(
        self, *origin_size
    ) -> typing.Tuple[typing.Tuple, typing.Tuple]:
        # convert to real size
        logger.debug(f"origin size: ({origin_size})")
        size_h, size_w = self.convert(*origin_size, *self.size)
        logger.debug(f"size: ({size_h}, {size_w})")
        offset_h, offset_w = self.convert(*origin_size, *self.offset)
        logger.debug(f"offset: {offset_h}, {offset_w}")
        height_range, width_range = (
            (int(offset_h), int(offset_h + size_h)),
            (int(offset_w), int(offset_w + size_w)),
        )
        logger.debug(f"final range h: {height_range}, w: {width_range}")
        return height_range, width_range


class CropHook(_AreaBaseHook):
    """ this hook was built for cropping frames, eg: keep only a half of origin frame """

    def do(self, frame: VideoFrame, *_, **__) -> typing.Optional[VideoFrame]:
        super().do(frame, *_, **__)

        height_range, width_range = self.convert_size_and_offset(*frame.data.shape)
        # ignore the rest of this frame
        # same as IgnoreHook
        frame.data[: height_range[0]] = 0
        frame.data[height_range[1] :] = 0
        frame.data[: width_range[0]] = 0
        frame.data[width_range[1] :] = 0
        return frame


class IgnoreHook(_AreaBaseHook):
    """ ignore some area of frames """

    def do(self, frame: VideoFrame, *_, **__) -> typing.Optional[VideoFrame]:
        super().do(frame, *_, **__)

        height_range, width_range = self.convert_size_and_offset(*frame.data.shape)
        # ignore this area
        frame.data[
            height_range[0] : height_range[1], width_range[0] : width_range[1]
        ] = 0
        return frame


# --- inner hook end ---


class FrameSaveHook(BaseHook):
    """ add this hook, and save all the frames you want to specific dir """

    def __init__(self, target_dir: str, *_, **__):
        super().__init__(*_, **__)

        # init target dir
        self.target_dir = target_dir
        os.makedirs(target_dir, exist_ok=True)

        logger.debug(f"target dir: {target_dir}")

    def do(self, frame: VideoFrame, *_, **__) -> typing.Optional[VideoFrame]:
        super().do(frame, *_, **__)
        safe_timestamp = str(frame.timestamp).replace(".", "_")
        frame_name = f"{frame.frame_id}({safe_timestamp}).png"
        target_path = os.path.join(self.target_dir, frame_name)
        cv2.imwrite(target_path, frame.data)
        logger.debug(f"frame saved to {target_path}")
        return frame


class InterestPointHook(BaseHook):
    """ use ORB detector to get the number of interest points """

    def __init__(self, *_, **__):
        super().__init__(*_, **__)
        self._orb = cv2.ORB_create()

    def do(self, frame: VideoFrame, *_, **__) -> typing.Optional[VideoFrame]:
        super().do(frame, *_, **__)
        kp = self._orb.detect(frame.data, None)
        self.result[frame.frame_id] = len(kp)
        return frame


class InvalidFrameDetectHook(BaseHook):
    def __init__(self, *_, **__):
        super(InvalidFrameDetectHook, self).__init__(*_, **__)
        raise DeprecationWarning("you'd better use EmptyFrameDetectHook instead")


class TemplateCompareHook(BaseHook):
    def __init__(self, template_dict: typing.Dict[str, str], *args, **kwargs):
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

    def do(self, frame: VideoFrame, *_, **__) -> typing.Optional[VideoFrame]:
        super().do(frame, *_, **__)
        for each_template_name, each_template_path in self.template_dict.items():
            self.fi.load_template(each_template_name, each_template_path)
        res = self.fi.find(str(frame.frame_id), target_pic_object=frame.data)
        logger.debug(f"compare with template {self.template_dict}: {res}")
        self.result[frame.frame_id] = res
        return frame
