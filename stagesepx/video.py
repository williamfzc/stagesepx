import os
import tempfile
import typing

import cv2
import imageio_ffmpeg
import numpy as np
from loguru import logger
from moviepy import VideoFileClip

from stagesepx import toolbox

if typing.TYPE_CHECKING:
    from stagesepx.hook import BaseHook


class VideoFrame(object):
    def __init__(self, frame_id: int, timestamp: float, data: np.ndarray):
        self.frame_id: int = frame_id
        self.timestamp: float = timestamp
        self.data: np.ndarray = data

    def __str__(self):
        return f"<VideoFrame id={self.frame_id} timestamp={self.timestamp}>"

    @classmethod
    def init(cls, cap: cv2.VideoCapture, frame: np.ndarray) -> "VideoFrame":
        frame_id = toolbox.get_current_frame_id(cap)
        timestamp = toolbox.get_current_frame_time(cap)
        grey = toolbox.turn_grey(frame)
        logger.debug(f"new a frame: {frame_id}({timestamp})")
        return VideoFrame(frame_id, timestamp, grey)

    def copy(self):
        return VideoFrame(self.frame_id, self.timestamp, self.data[:])

    def contain_image(
        self, *, image_path: str = None, image_object: np.ndarray = None, **kwargs
    ) -> typing.Dict[str, typing.Any]:
        assert image_path or (
            image_object is not None
        ), "should fill image_path or image_object"

        if image_path:
            logger.debug(f"found image path, use it first: {image_path}")
            return toolbox.match_template_with_path(image_path, self.data, **kwargs)
        image_object = toolbox.turn_grey(image_object)
        return toolbox.match_template_with_object(image_object, self.data, **kwargs)


class _BaseFrameOperator(object):
    def __init__(self, video: "VideoObject"):
        # pointer
        self.cur_ptr: int = 0
        self.video: VideoObject = video

    def get_frame_by_id(self, frame_id: int) -> typing.Optional[VideoFrame]:
        raise NotImplementedError

    def get_length(self) -> int:
        return self.video.frame_count


class MemFrameOperator(_BaseFrameOperator):
    def get_frame_by_id(self, frame_id: int) -> typing.Optional[VideoFrame]:
        if frame_id > self.get_length():
            return None
        # list starts from zero, but frame starts from one
        frame_id = frame_id - 1
        return self.video.data[frame_id].copy()


class FileFrameOperator(_BaseFrameOperator):
    def get_frame_by_id(self, frame_id: int) -> typing.Optional[VideoFrame]:
        if frame_id > self.get_length():
            return None
        with toolbox.video_capture(self.video.path) as cap:
            toolbox.video_jump(cap, frame_id)
            success, frame = cap.read()
            video_frame = VideoFrame.init(cap, frame) if success else None
        return video_frame


class VideoObject(object):
    def __init__(
        self,
        path: typing.Union[str, os.PathLike],
        pre_load: bool = None,
        fps: int = None,
        *_,
        **__,
    ):
        assert os.path.isfile(path), f"video {path} not existed"
        self.path: str = str(path)
        self.data: typing.Optional[typing.Tuple[VideoFrame]] = tuple()
        self._hook_list: typing.List["BaseHook"] = []

        self.fps: int = fps
        if fps:
            video_path = os.path.join(tempfile.mkdtemp(), f"tmp_{fps}.mp4")
            logger.debug(f"convert video, and bind path to {video_path}")
            toolbox.fps_convert(
                fps, self.path, video_path, imageio_ffmpeg.get_ffmpeg_exe()
            )
            self.path = video_path

        with toolbox.video_capture(self.path) as cap:
            self.frame_count = toolbox.get_frame_count(cap)
            self.frame_size = toolbox.get_frame_size(cap)

        if pre_load is not None:
            logger.warning(
                f"`pre_load` has been deprecated. use `video.load_frames()` instead"
            )
        logger.info(
            f"video object generated, length: {self.frame_count}, size: {self.frame_size}"
        )

    def __str__(self):
        return f"<VideoObject path={self.path}>"

    __repr__ = __str__

    def sync_timestamp(self):
        vid = VideoFileClip(self.path)

        # moviepy start from 0, 0.0
        # but stagesepx is 1, 0.0
        assert self.data, "load_frames() first"
        for frame_id, (timestamp, _) in enumerate(vid.iter_frames(with_times=True)):
            if frame_id >= len(self.data):
                # ignore the rest
                break
            frame_id_real = frame_id + 1
            if not self.data[frame_id].timestamp:
                logger.debug(f"fix frame {frame_id_real}'s timestamp: {timestamp}")
                self.data[frame_id].timestamp = timestamp
        logger.info("sync timestamp with moviepy finished")

    def add_preload_hook(self, new_hook: "BaseHook"):
        """this hook only will be executed when preload"""
        self._hook_list.append(new_hook)

    def clean_frames(self):
        self.data = tuple()

    def load_frames(self, *args, **kwargs):
        logger.info(f"start loading {self.path} to memory ...")

        data: typing.List[VideoFrame] = []
        with toolbox.video_capture(self.path) as cap:
            # the first
            success, frame = cap.read()
            while success:
                frame_object = VideoFrame.init(cap, frame)
                # apply hooks
                for each_hook in self._hook_list:
                    frame_object = each_hook.do(frame_object, *args, **kwargs)
                data.append(frame_object)
                # read the next one
                success, frame = cap.read()

        # calculate memory cost
        each_cost = data[0].data.nbytes
        logger.debug(f"single frame cost: {each_cost} bytes")
        total_cost = each_cost * self.frame_count
        logger.debug(f"total frame cost: {total_cost} bytes")

        # lock the order
        self.data = tuple(data)
        # fix the length ( the last frame may be broken sometimes )
        self.frame_count = len(data)
        # and size (reversed, see: https://github.com/williamfzc/stagesepx/issues/132)
        self.frame_size = data[0].data.shape[::-1]
        logger.info(
            f"frames loaded. frame count: {self.frame_count}, size: {self.frame_size}, memory cost: {total_cost} bytes"
        )

        # sync timestamp for some newer versions opencv
        # see: #178, #181
        self.sync_timestamp()

    def _read_from_file(self) -> typing.Generator[VideoFrame, None, None]:
        with toolbox.video_capture(self.path) as cap:
            success, frame = cap.read()
            while success:
                yield VideoFrame.init(cap, frame)
                success, frame = cap.read()

    def _read_from_mem(self) -> typing.Generator[VideoFrame, None, None]:
        for each_frame in self.data:
            yield each_frame

    def _read(self) -> typing.Generator[VideoFrame, None, None]:
        if self.data:
            yield from self._read_from_mem()
        else:
            yield from self._read_from_file()

    def get_iterator(self) -> typing.Generator[VideoFrame, None, None]:
        return self._read()

    def get_operator(self) -> _BaseFrameOperator:
        if self.data:
            return MemFrameOperator(self)
        return FileFrameOperator(self)

    def __iter__(self):
        return self.get_iterator()
