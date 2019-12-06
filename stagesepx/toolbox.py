import cv2
import contextlib
import time
import random
import typing
import math
import os
import numpy as np
import subprocess
from base64 import b64encode
from skimage.filters import threshold_otsu
from skimage.metrics import structural_similarity as origin_compare_ssim
from skimage.metrics import normalized_root_mse as compare_nrmse
from skimage.metrics import peak_signal_noise_ratio as compare_psnr
from skimage.feature import hog, local_binary_pattern
from loguru import logger
from findit import FindIt


# DO NOT IMPORT ANYTHING FROM STAGESEPX HERE
# MAKE TOOLBOX STATIC


@contextlib.contextmanager
def video_capture(video_path: str):
    video_cap = cv2.VideoCapture(video_path)
    try:
        yield video_cap
    finally:
        video_cap.release()


def video_jump(video_cap: cv2.VideoCapture, frame_id: int):
    # IMPORTANT:
    # - frame is a range actually
    # - frame 1 's timestamp is the end of this frame
    #
    # video_jump(cap, 1) means: moving the pointer to the start point of frame 1 => the end point of frame 0

    video_cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id - 1)
    logger.debug(
        f"current pointer: {get_current_frame_id(video_cap)}({get_current_frame_time(video_cap)})"
    )


def compare_ssim(pic1: np.ndarray, pic2: np.ndarray) -> float:
    pic1, pic2 = [turn_grey(i) for i in [pic1, pic2]]
    return origin_compare_ssim(pic1, pic2)


def multi_compare_ssim(
    pic1_list: typing.List, pic2_list: typing.List
) -> typing.List[float]:
    # avoid import loop
    from stagesepx.video import VideoFrame

    if isinstance(pic1_list[0], VideoFrame):
        pic1_list = [i.data for i in pic1_list]
    if isinstance(pic2_list[0], VideoFrame):
        pic2_list = [i.data for i in pic2_list]
    return [compare_ssim(a, b) for a, b in zip(pic1_list, pic2_list)]


def get_current_frame_id(video_cap: cv2.VideoCapture) -> int:
    return int(video_cap.get(cv2.CAP_PROP_POS_FRAMES))


def get_current_frame_time(video_cap: cv2.VideoCapture) -> float:
    return video_cap.get(cv2.CAP_PROP_POS_MSEC) / 1000


def imread(img_path: str, *_, **__) -> np.ndarray:
    """ wrapper of cv2.imread """
    assert os.path.isfile(img_path), f"file {img_path} is not existed"
    return cv2.imread(img_path, *_, **__)


def get_frame_time(
    video_cap: cv2.VideoCapture, frame_id: int, recover: bool = None
) -> float:
    cur = get_current_frame_id(video_cap)
    video_jump(video_cap, frame_id + 1)
    result = get_current_frame_time(video_cap)
    logger.debug(f"frame {frame_id} -> {result}")

    if recover:
        video_jump(video_cap, cur + 1)
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


def get_frame(
    video_cap: cv2.VideoCapture, frame_id: int, recover: bool = None
) -> np.ndarray:
    cur = get_current_frame_id(video_cap)
    video_jump(video_cap, frame_id)
    ret, frame = video_cap.read()
    assert ret, f"read frame failed, frame id: {frame_id}"

    if recover:
        video_jump(video_cap, cur + 1)
    return frame


def turn_grey(old: np.ndarray) -> np.ndarray:
    try:
        return cv2.cvtColor(old, cv2.COLOR_RGB2GRAY)
    except cv2.error:
        return old


def turn_binary(old: np.ndarray) -> np.ndarray:
    # TODO not always work
    grey = turn_grey(old)
    thresh = threshold_otsu(grey)
    return (grey > thresh).astype(np.uint8)


def turn_hog_desc(old: np.ndarray) -> np.ndarray:
    fd, _ = hog(
        old,
        orientations=8,
        pixels_per_cell=(16, 16),
        cells_per_block=(1, 1),
        block_norm="L2-Hys",
        visualize=True,
    )

    # also available with opencv-python
    # hog = cv2.HOGDescriptor()
    # return hog.compute(old)
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
    lbp = local_binary_pattern(grey, n_points, radius, method="default")
    return lbp


def turn_blur(old: np.ndarray) -> np.ndarray:
    # TODO these args are locked and can not be changed
    return cv2.GaussianBlur(old, (7, 7), 0)


def sharpen_frame(old: np.ndarray) -> np.ndarray:
    """
    refine the edges of an image

    - https://answers.opencv.org/question/121205/how-to-refine-the-edges-of-an-image/
    - https://stackoverflow.com/questions/4993082/how-to-sharpen-an-image-in-opencv

    :param old:
    :return:
    """

    # TODO these args are locked and can not be changed
    blur = turn_blur(old)
    smooth = cv2.addWeighted(blur, 1.5, old, -0.5, 0)
    canny = cv2.Canny(smooth, 50, 150)
    return canny


def calc_mse(pic1: np.ndarray, pic2: np.ndarray) -> float:
    # MSE: https://en.wikipedia.org/wiki/Mean_squared_error
    # return np.sum((pic1.astype('float') - pic2.astype('float')) ** 2) / float(pic1.shape[0] * pic2.shape[1])
    return compare_nrmse(pic1, pic2)


def calc_psnr(pic1: np.ndarray, pic2: np.ndarray) -> float:
    # PSNR: https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio
    psnr = compare_psnr(pic1, pic2)
    # when err == 0, psnr will be 'inf'
    if math.isinf(psnr):
        psnr = 100.0
    # normalize
    return psnr / 100


def compress_frame(
    old: np.ndarray,
    compress_rate: float = None,
    target_size: typing.Tuple[int, int] = None,
    not_grey: bool = None,
    interpolation: int = None,
    *_,
    **__,
) -> np.ndarray:
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

    if not interpolation:
        interpolation = cv2.INTER_AREA
    # target size first
    if target_size:
        return cv2.resize(target, target_size, interpolation=interpolation)
    # else, use compress rate
    # default rate is 1 (no compression)
    if not compress_rate:
        return target
    return cv2.resize(
        target, (0, 0), fx=compress_rate, fy=compress_rate, interpolation=interpolation
    )


def get_timestamp_str() -> str:
    time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
    salt = random.randint(10, 99)
    return f"{time_str}{salt}"


def np2b64str(frame: np.ndarray) -> str:
    buffer = cv2.imencode(".png", frame)[1].tostring()
    return b64encode(buffer).decode()


def fps_convert(
    target_fps: int, source_path: str, target_path: str, ffmpeg_exe: str = None
) -> int:
    # for portable ffmpeg
    if not ffmpeg_exe:
        ffmpeg_exe = r"ffmpeg"
    command: typing.List[str] = [
        ffmpeg_exe,
        "-i",
        source_path,
        "-r",
        str(target_fps),
        target_path,
    ]
    logger.debug(f"convert video: {command}")
    return subprocess.check_call(command)


def match_template_with_object(
    template: np.ndarray,
    target: np.ndarray,
    engine_template_cv_method_name: str = None,
    **kwargs,
) -> typing.Dict[str, typing.Any]:
    # change the default method
    if not engine_template_cv_method_name:
        engine_template_cv_method_name = "cv2.TM_CCOEFF_NORMED"

    fi = FindIt(
        engine=["template"],
        engine_template_cv_method_name=engine_template_cv_method_name,
        **kwargs,
    )
    # load template
    fi_template_name = "default"
    fi.load_template(fi_template_name, pic_object=template)

    result = fi.find(target_pic_name="", target_pic_object=target, **kwargs)
    logger.debug(f"findit result: {result}")
    return result["data"][fi_template_name]["TemplateEngine"]


def match_template_with_path(
    template: str, target: np.ndarray, **kwargs
) -> typing.Dict[str, typing.Any]:
    assert os.path.isfile(template), f"image {template} not existed"
    template_object = turn_grey(imread(template))
    return match_template_with_object(template_object, target, **kwargs)
