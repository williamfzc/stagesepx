from stagesepx.video import VideoObject, VideoFrame
from stagesepx.hook import ExampleHook
import os
import pathlib


PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
VIDEO_PATH = os.path.join(PROJECT_PATH, "demo.mp4")
VIDEO_PATHLIB_PATH = pathlib.Path(VIDEO_PATH)
IMAGE_NAME = "demo.jpg"
IMAGE_PATH = os.path.join(PROJECT_PATH, IMAGE_NAME)


def test_read_from_file():
    v = VideoObject(VIDEO_PATH)
    count = 0
    for f in v:
        assert isinstance(f, VideoFrame)
        count += 1
    assert count == 30


def test_pathlib_path():
    v = VideoObject(VIDEO_PATHLIB_PATH)
    count = 0
    for f in v:
        assert isinstance(f, VideoFrame)
        count += 1
    assert count == 30


def test_read_from_mem():
    v = VideoObject(VIDEO_PATH)
    print(str(v))
    v.load_frames()
    count = 0
    for f in v:
        assert isinstance(f, VideoFrame)
        print(str(f))
        count += 1
    assert count == 30

    v.clean_frames()
    assert not v.data


def test_convert_first():
    v = VideoObject(VIDEO_PATH, fps=30)
    v.load_frames()
    assert len(v.data) == 36


def test_contain_image():
    v = VideoObject(VIDEO_PATH)
    v.load_frames()
    ret = v.data[0].contain_image(image_path=IMAGE_PATH)
    assert ret["ok"]


def test_preload_with_hook():
    v = VideoObject(VIDEO_PATH)
    hook = ExampleHook()
    v.add_preload_hook(hook)
    v.load_frames()


def test_sync_timestamp():
    v = VideoObject(VIDEO_PATH)
    v.load_frames()
    v.sync_timestamp()
