import cv2
import contextlib
import time
import random
import typing
import numpy as np
from skimage.filters import threshold_otsu
from skimage.measure import compare_ssim as origin_compare_ssim
from skimage.feature import hog, local_binary_pattern


@contextlib.contextmanager
def video_capture(video_path: str):
    video_cap = cv2.VideoCapture(video_path)
    try:
        yield video_cap
    finally:
        video_cap.release()


def video_jump(video_cap: cv2.VideoCapture, frame_id: int):
    video_cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id - 1)


def compare_ssim(pic1: np.ndarray, pic2: np.ndarray) -> float:
    pic1, pic2 = [turn_grey(i) for i in [pic1, pic2]]
    return origin_compare_ssim(pic1, pic2)


def get_current_frame_id(video_cap: cv2.VideoCapture) -> int:
    return int(video_cap.get(cv2.CAP_PROP_POS_FRAMES))


def get_current_frame_time(video_cap: cv2.VideoCapture) -> float:
    return video_cap.get(cv2.CAP_PROP_POS_MSEC) / 1000


def get_frame_time(video_cap: cv2.VideoCapture, frame_id: int, recover: bool = None) -> float:
    cur = get_current_frame_id(video_cap)
    video_jump(video_cap, frame_id)
    result = get_current_frame_time(video_cap)

    if recover:
        video_jump(video_cap, cur)
    return result


def get_frame_count(video_cap: cv2.VideoCapture) -> int:
    # NOT always accurate, see:
    # https://stackoverflow.com/questions/31472155/python-opencv-cv2-cv-cv-cap-prop-frame-count-get-wrong-numbers
    return int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))


def get_frame_size(video_cap: cv2.VideoCapture) -> typing.Tuple[int, int]:
    """ return size of frame: (width, height) """
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


def turn_lbp_desc(old: np.ndarray, radius: int = None) -> np.ndarray:
    if not radius:
        radius = 3
    n_points = 8 * radius

    grey = turn_grey(old)
    lbp = local_binary_pattern(grey, n_points, radius, method='default')
    return lbp


def compress_frame(old: np.ndarray,
                   compress_rate: float = None,
                   target_size: typing.Tuple[int, int] = None,
                   not_grey: bool = None,
                   interpolation: int = None,
                   *_, **__) -> np.ndarray:
    """
    Compress frame

    :param old:
        origin frame

    :param compress_rate:
        before_pic * compress_rate = after_pic. default to 1 (no compression)
        eg: 0.2 means 1/5 size of before_pic

    :param target_size:
        tuple. (100, 200) means compressing before_pic to 100x200

    :param not_grey:
        convert into grey if True

    :param interpolation:
    :return:
    """

    target = turn_grey(old) if not not_grey else old
    target = cv2.bilateralFilter(target, 9, 75, 75)

    if not interpolation:
        interpolation = cv2.INTER_AREA
    # target size first
    if target_size:
        return cv2.resize(target, target_size, interpolation=interpolation)
    # else, use compress rate
    # default rate is 1 (no compression)
    if not compress_rate:
        return target
    return cv2.resize(target, (0, 0), fx=compress_rate, fy=compress_rate, interpolation=interpolation)


def get_timestamp_str() -> str:
    time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
    salt = random.randint(10, 99)
    return f'{time_str}{salt}'


if __name__ == '__main__':
    t = cv2.imread('../1.png', cv2.IMREAD_GRAYSCALE)
    turn_surf_desc(t)
