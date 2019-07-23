import cv2
import contextlib
import time
import random
import typing
import numpy as np
from skimage.filters import threshold_otsu
from skimage.measure import compare_ssim
from skimage.feature import hog

compare_ssim = compare_ssim


@contextlib.contextmanager
def video_capture(video_path: str):
    video_cap = cv2.VideoCapture(video_path)
    try:
        yield video_cap
    finally:
        video_cap.release()


def video_jump(video_cap: cv2.VideoCapture, frame_id: int):
    video_cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id - 1)


def get_current_frame_id(video_cap: cv2.VideoCapture) -> int:
    return int(video_cap.get(cv2.CAP_PROP_POS_FRAMES))


def get_current_frame_time(video_cap: cv2.VideoCapture) -> float:
    return video_cap.get(cv2.CAP_PROP_POS_MSEC) / 1000


def get_frame_count(video_cap: cv2.VideoCapture) -> int:
    return int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))


def get_frame_size(video_cap: cv2.VideoCapture) -> typing.Tuple[int, int]:
    h = video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    w = video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    return int(w), int(h)


def get_frame(video_cap: cv2.VideoCapture, frame_id: int, recover: bool = None) -> np.ndarray:
    cur = get_current_frame_id(video_cap)
    video_jump(video_cap, frame_id)
    ret, frame = video_cap.read()
    assert ret, f'read frame failed, frame id: {frame_id}'

    if recover:
        video_jump(video_cap, cur)
    return frame


def turn_grey(old: np.ndarray) -> np.ndarray:
    try:
        return cv2.cvtColor(old, cv2.COLOR_RGB2GRAY)
    except cv2.error:
        return old


def turn_binary(old: np.ndarray) -> np.ndarray:
    thresh = threshold_otsu(old)
    return old > thresh


def turn_hog_desc(old: np.ndarray) -> np.ndarray:
    fd, _ = hog(
        old,
        orientations=8,
        pixels_per_cell=(16, 16),
        cells_per_block=(1, 1),
        block_norm='L2-Hys',
        visualize=True)
    return fd


def turn_surf_desc(old: np.ndarray, hessian: int = None) -> np.ndarray:
    if not hessian:
        hessian = 200
    surf = cv2.xfeatures2d.SURF_create(hessian)
    _, desc = surf.detectAndCompute(old, None)
    return desc


def compress_frame(old: np.ndarray, compress_rate: float = None, interpolation: int = None) -> np.ndarray:
    if not compress_rate:
        compress_rate = 0.2
    if not interpolation:
        interpolation = cv2.INTER_AREA

    grey = turn_grey(old)
    return cv2.resize(grey, (0, 0), fx=compress_rate, fy=compress_rate, interpolation=interpolation)


def get_timestamp_str() -> str:
    time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
    salt = random.randint(10, 99)
    return f'{time_str}{salt}'


if __name__ == '__main__':
    t = cv2.imread('../1.png', cv2.IMREAD_GRAYSCALE)
    turn_surf_desc(t)
