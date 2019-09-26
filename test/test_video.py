from stagesepx.video import VideoObject, VideoFrame
import os


PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
VIDEO_PATH = os.path.join(PROJECT_PATH, "demo.mp4")


def test_read_from_file():
    v = VideoObject(VIDEO_PATH)
    count = 0
    for f in v:
        assert isinstance(f, VideoFrame)
        count += 1
    assert count == 30


def test_read_from_mem():
    v = VideoObject(VIDEO_PATH)
    v.load_frames()
    count = 0
    for f in v:
        assert isinstance(f, VideoFrame)
        count += 1
    assert count == 30
