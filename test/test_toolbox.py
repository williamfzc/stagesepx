import os

from stagesepx import toolbox

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
IMAGE_NAME = "demo.jpg"
IMAGE_PATH = os.path.join(PROJECT_PATH, IMAGE_NAME)
VIDEO_NAME = "demo.mp4"
VIDEO_PATH = os.path.join(PROJECT_PATH, VIDEO_NAME)
assert os.path.isfile(IMAGE_PATH), f"{IMAGE_NAME} not existed!"
assert os.path.isfile(VIDEO_PATH), f"{VIDEO_PATH} not existed!"


def test_turn_blur():
    image = toolbox.imread(IMAGE_PATH)
    grey = toolbox.turn_grey(image)
    toolbox.turn_blur(grey)


def test_turn_grey():
    image = toolbox.imread(IMAGE_PATH)
    toolbox.turn_grey(image)


def test_turn_binary():
    image = toolbox.imread(IMAGE_PATH)
    toolbox.turn_binary(image)


def test_turn_lbp_desc():
    image = toolbox.imread(IMAGE_PATH)
    toolbox.turn_lbp_desc(image)


def test_get_frame():
    with toolbox.video_capture(VIDEO_PATH) as cap:
        first = 5
        second = 8

        toolbox.video_jump(cap, first)
        actual = toolbox.get_frame_time(cap, first)
        should = toolbox.get_current_frame_time(cap)

        # should be frame 5
        assert actual == should
        assert actual - 0.16 < 0.01

        # 5 -> 8 -> 5
        frame = toolbox.get_frame(cap, second, True)
        assert frame is not None
        # grab, and recover
        # the next frame will be 5
        # the current frame is 4
        assert toolbox.get_current_frame_id(cap) == first - 1

        # 5 -> 8
        frame = toolbox.get_frame(cap, second)
        assert frame is not None
        assert toolbox.get_current_frame_id(cap) == second

        #
        cur_time = toolbox.get_current_frame_time(cap)
        toolbox.get_frame_time(cap, second, True)
        assert toolbox.get_current_frame_time(cap) == cur_time


def test_compress():
    image = toolbox.imread(IMAGE_PATH)
    frame = toolbox.compress_frame(image, target_size=(100, 100))
    assert frame.shape == (100, 100)


def test_convert_video():
    target_fps: int = 30
    ret = toolbox.fps_convert(
        target_fps, VIDEO_PATH, os.path.join(PROJECT_PATH, f"{target_fps}.mp4")
    )
    assert not ret


def test_match_template():
    image1 = toolbox.imread(IMAGE_PATH)
    image2 = toolbox.imread(IMAGE_PATH)
    ret = toolbox.match_template_with_object(image1, image2)
    assert ret["ok"]

    ret = toolbox.match_template_with_path(IMAGE_PATH, image2)
    assert ret["ok"]
