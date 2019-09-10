from stagesepx.cutter import VideoCutter, VideoCutResult
import os

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
VIDEO_PATH = os.path.join(PROJECT_PATH, 'demo.mp4')
RESULT_DIR = os.path.join(PROJECT_PATH, 'cut_result')
IMAGE_NAME = 'demo.jpg'
IMAGE_PATH = os.path.join(PROJECT_PATH, IMAGE_NAME)
assert os.path.isfile(IMAGE_PATH), f'{IMAGE_NAME} not existed!'


def test_default():
    cutter = VideoCutter()
    res = cutter.cut(VIDEO_PATH)
    stable, unstable = res.get_range()
    assert len(stable) == 3, 'count of stable range is not correct'

    data_home = res.pick_and_save(stable, 5, to_dir=RESULT_DIR)
    assert data_home == RESULT_DIR
    assert os.path.isdir(data_home), 'result dir not existed'
    return res


def test_limit():
    cutter = VideoCutter()
    res = cutter.cut(VIDEO_PATH)
    stable, unstable = res.get_range(limit=3)
    # when limit=3, final stage should be ignored.
    assert len(stable) == 1, 'count of stable range is not correct'


def test_step():
    cutter = VideoCutter(step=2)
    res = cutter.cut(VIDEO_PATH)
    stable, unstable = res.get_range()
    # when limit=3, final stage should be ignored.
    assert len(stable) == 1, 'count of stable range is not correct'


def test_dump_and_load():
    cutter = VideoCutter()
    res = cutter.cut(VIDEO_PATH)
    json_path = 'cutter_result.json'
    res.dump(json_path)

    res_from_file = VideoCutResult.load(json_path)
    assert res.dumps() == res_from_file.dumps()


def test_prune():
    cutter = VideoCutter()
    res = cutter.cut(VIDEO_PATH)
    stable, unstable = res.get_range()
    assert len(stable) == 3, 'count of stable range is not correct'

    data_home = res.pick_and_save(stable, 5, prune=0.99)
    assert os.path.isdir(data_home), 'result dir not existed'


def test_cut_range():
    cutter = VideoCutter()
    res = cutter.cut(VIDEO_PATH)
    stable, _ = res.get_range()
    stable[0].contain_image(IMAGE_PATH)
    stable[0].is_loop(0.95)
