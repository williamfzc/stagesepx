import os
import typing
import cv2
import numpy as np
from loguru import logger

from stagesepx import toolbox


class VideoFrame(object):
    def __init__(self, frame_id: int, timestamp: float, data: np.ndarray):
        self.frame_id = frame_id
        self.timestamp = timestamp
        self.data = data

    def __str__(self):
        return f"<VideoFrame id={self.frame_id} timestamp={self.timestamp}>"

    @classmethod
    def init(cls, cap: cv2.VideoCapture, frame: np.ndarray) -> "VideoFrame":
        frame_id = toolbox.get_current_frame_id(cap)
        timestamp = toolbox.get_current_frame_time(cap)
        grey = toolbox.turn_grey(frame)
        return VideoFrame(frame_id, timestamp, grey)

    def copy(self):
        return VideoFrame(self.frame_id, self.timestamp, self.data[:])


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
        path: typing.Union[bytes, str, os.PathLike],
        pre_load: bool = None,
        *_,
        **__,
    ):
        assert os.path.isfile(path), f"video [{path}] not existed"
        self.path: str = str(path)
        self.data: typing.Optional[typing.Tuple[VideoFrame]] = tuple()

        with toolbox.video_capture(path) as cap:
            self.frame_count = toolbox.get_frame_count(cap)
            self.frame_size = toolbox.get_frame_size(cap)

        if pre_load:
            self.load_frames()

    def __str__(self):
        return f"<VideoObject path={self.path}>"

    __repr__ = __str__

    def clean_frames(self):
        self.data = tuple()

    def load_frames(self):
        # TODO full frames list can be very huge, for some devices
        logger.info(f"start loading {self.path} to memory ...")

        data: typing.List[VideoFrame] = []
        with toolbox.video_capture(self.path) as cap:
            success, frame = cap.read()
            while success:
                frame_object = VideoFrame.init(cap, frame)
                data.append(frame_object)
                success, frame = cap.read()

        # calculate memory cost
        each_cost = data[0].data.nbytes
        logger.debug(f"single frame cost: {each_cost} bytes")
        total_cost = each_cost * self.frame_count
        logger.debug(f"total frame cost: {total_cost} bytes")
        logger.info(
            f"frames loaded. frame count: {self.frame_count}. memory cost: {total_cost} bytes"
        )

        # lock the order
        self.data = tuple(data)

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
