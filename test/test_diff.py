from stagesepx.cutter import VideoCutter
import os
import pprint

from stagesepx.cutter.cut_result import VideoCutResultDiff
from stagesepx.hook import CropHook

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))

# use same video?
VIDEO_PATH = os.path.join(PROJECT_PATH, "demo.mp4")
ANOTHER_VIDEO_PATH = os.path.join(PROJECT_PATH, "demo.mp4")


def test_diff():
    cutter = VideoCutter()
    res = cutter.cut(VIDEO_PATH)
    res1 = cutter.cut(ANOTHER_VIDEO_PATH)

    for each in (res, res1):
        stable, _ = each.get_range()
        res.pick_and_save(stable, 3)

    diff: VideoCutResultDiff = res.diff(res1, frame_count=5)
    pprint.pprint(diff.data)
    assert diff.data
    assert not diff.any_stage_lost()


def test_diff_with_hook():
    cutter = VideoCutter()
    res = cutter.cut(VIDEO_PATH)
    res1 = cutter.cut(ANOTHER_VIDEO_PATH)

    for each in (res, res1):
        stable, _ = each.get_range()
        res.pick_and_save(stable, 3)

    hook = [CropHook(size=(0.5, 0.5))]

    diff = res.diff(res1, pre_hooks=hook, frame_count=5)
    pprint.pprint(diff.data)
    assert diff.data
    assert not diff.any_stage_lost()
