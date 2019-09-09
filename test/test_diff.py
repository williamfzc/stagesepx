from stagesepx.cutter import VideoCutter
import os
import pprint

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))

# use same video?
VIDEO_PATH = os.path.join(PROJECT_PATH, 'demo.mp4')
ANOTHER_VIDEO_PATH = os.path.join(PROJECT_PATH, 'demo.mp4')


def test_diff():
    cutter = VideoCutter()
    res = cutter.cut(VIDEO_PATH)
    res1 = cutter.cut(ANOTHER_VIDEO_PATH)

    for each in (res, res1):
        stable, _ = each.get_range()
        res.pick_and_save(stable, 3)

    diff_dict = res.diff(res1, frame_count=5)
    pprint.pprint(diff_dict)
    assert diff_dict
