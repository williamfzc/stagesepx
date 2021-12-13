from stagesepx.cutter import VideoCutter, VideoCutResult
from stagesepx.cutter.cut_result import VideoCutResultDiff
from stagesepx.video import VideoObject
import os
import shutil
import numpy as np

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
VIDEO_PATH = os.path.join(PROJECT_PATH, "demo.mp4")
RESULT_DIR = os.path.join(PROJECT_PATH, "cut_result")
IMAGE_NAME = "demo.jpg"
IMAGE_PATH = os.path.join(PROJECT_PATH, IMAGE_NAME)
assert os.path.isfile(IMAGE_PATH), f"{IMAGE_NAME} not existed!"


def test_default():
    cutter = VideoCutter()
    res = cutter.cut(VIDEO_PATH)
    stable, unstable = res.get_range()
    assert len(stable) == 3, "count of stable range is not correct"

    if os.path.exists(RESULT_DIR):
        shutil.rmtree(RESULT_DIR)

    data_home = res.pick_and_save(stable, 5, to_dir=RESULT_DIR)
    assert data_home == RESULT_DIR
    assert os.path.isdir(data_home), "result dir not existed"

    # run again to test covering result
    data_home = res.pick_and_save(stable, 5, to_dir=RESULT_DIR)
    assert data_home == RESULT_DIR
    assert os.path.isdir(data_home), "result dir not existed"

    sub_dir_0 = os.path.join(data_home, "0")
    assert len(os.listdir(sub_dir_0)) == 10
    return res


def test_limit():
    cutter = VideoCutter()
    res = cutter.cut(VIDEO_PATH)
    stable, unstable = res.get_range(limit=3)
    # when limit=3, final stage should be ignored.
    assert len(stable) == 1, "count of stable range is not correct"


def test_step():
    cutter = VideoCutter(step=2)
    res = cutter.cut(VIDEO_PATH)
    stable, unstable = res.get_range()
    # when limit=3, final stage should be ignored.
    assert len(stable) == 2, "count of stable range is not correct"


def test_dump_and_load():
    cutter = VideoCutter()
    res = cutter.cut(VIDEO_PATH)
    json_path = "cutter_result.json"
    res.dump(json_path)

    res_from_file = VideoCutResult.load(json_path)
    assert res.dumps() == res_from_file.dumps()


def test_prune():
    cutter = VideoCutter()
    res = cutter.cut(VIDEO_PATH)
    stable, unstable = res.get_range()
    assert len(stable) == 3, "count of stable range is not correct"

    data_home = res.pick_and_save(stable, 5, prune=0.99)
    assert os.path.isdir(data_home), "result dir not existed"

    # meaningful name
    data_home = res.pick_and_save(stable, 3, meaningful_name=True)
    assert data_home


def test_cut_range():
    cutter = VideoCutter()
    res = cutter.cut(VIDEO_PATH)
    stable, _ = res.get_range()
    stable[0].contain_image(IMAGE_PATH)
    stable[0].is_loop(0.95)


def test_cut_result():
    cutter = VideoCutter()
    v = VideoObject(VIDEO_PATH)
    res = cutter.cut(v)
    stable, _ = res.get_range()
    assert len(stable) == len(res.get_stable_range())
    assert isinstance(res.diff(res, auto_merge=True), VideoCutResultDiff)
    assert isinstance(res.thumbnail(stable[0]), np.ndarray)
    assert isinstance(res.thumbnail(stable[0], is_vertical=True), np.ndarray)
    assert isinstance(res.thumbnail(stable[0], to_dir="somewhere"), np.ndarray)

    res.get_range_dynamic([4, 5], threshold=0.95)
    res.get_range_dynamic([1, 2], threshold=0.85)


def test_window():
    cutter = VideoCutter()
    v = VideoObject(VIDEO_PATH)
    res = cutter.cut(v, window_size=2, window_coefficient=2)
    assert res
