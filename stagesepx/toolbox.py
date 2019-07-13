import cv2
import contextlib
import time
import numpy as np
from skimage.filters import threshold_otsu
from skimage.measure import compare_ssim

compare_ssim = compare_ssim


@contextlib.contextmanager
def video_capture(video_path: str):
    video_cap = cv2.VideoCapture(video_path)
    try:
        yield video_cap
    finally:
        video_cap.release()


def video_jump(video_cap: cv2.VideoCapture, frame_id: int):
    video_cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)


def get_current_frame_id(video_cap: cv2.VideoCapture) -> int:
    return int(video_cap.get(cv2.CAP_PROP_POS_FRAMES))


def get_current_frame_time(video_cap: cv2.VideoCapture) -> float:
    return video_cap.get(cv2.CAP_PROP_POS_MSEC) / 1000


def get_frame(video_cap: cv2.VideoCapture, frame_id: int) -> np.ndarray:
    video_jump(video_cap, frame_id)
    ret, frame = video_cap.read()
    assert ret
    return frame


def turn_grey(old: np.ndarray) -> np.ndarray:
    try:
        return cv2.cvtColor(old, cv2.COLOR_RGB2GRAY)
    except cv2.error:
        return old


def turn_binary(old: np.ndarray) -> np.ndarray:
    thresh = threshold_otsu(old)
    return old > thresh


def compress_frame(old: np.ndarray, compress_rate: float = None, interpolation: int = None) -> np.ndarray:
    if not compress_rate:
        compress_rate = 0.2
    if not interpolation:
        interpolation = cv2.INTER_AREA

    grey = turn_grey(old)
    return cv2.resize(grey, (0, 0), fx=compress_rate, fy=compress_rate, interpolation=interpolation)


def get_timestamp_str() -> str:
    return str(time.time()).replace('.', '')
