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
    print(str(v))
    v.load_frames()
    count = 0
    for f in v:
        assert isinstance(f, VideoFrame)
        print(str(f))
        count += 1
    assert count == 30

    v = VideoObject(VIDEO_PATH, pre_load=True)
    v.clean_frames()
    assert not v.data
