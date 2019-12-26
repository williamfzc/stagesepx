from stagesepx.cutter import VideoCutter
from stagesepx.classifier import SVMClassifier
from stagesepx.reporter import Reporter
from stagesepx.hook import (
    ExampleHook,
    IgnoreHook,
    CropHook,
    FrameSaveHook,
    RefineHook,
    InterestPointHook,
    TemplateCompareHook,
    InvalidFrameDetectHook,
    _AreaBaseHook,
)

import os

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
VIDEO_PATH = os.path.join(PROJECT_PATH, "demo.mp4")
IMAGE_NAME = "demo.jpg"
IMAGE_PATH = os.path.join(PROJECT_PATH, IMAGE_NAME)
assert os.path.isfile(IMAGE_PATH)


def test_others():
    assert _AreaBaseHook.convert(200, 200, 100, 100) == (100, 100)
    try:
        InvalidFrameDetectHook()
    except DeprecationWarning:
        pass


def test_hook():
    # init hook
    hook = ExampleHook()
    hook1 = ExampleHook()
    hook2 = IgnoreHook(size=(0.5, 0.5))
    frame_home = os.path.join(PROJECT_PATH, "frame_save_dir")
    hook3 = FrameSaveHook(frame_home)
    hook4 = CropHook(size=(0.5, 0.5), offset=(0.0, 0.5))
    hook5 = RefineHook()
    hook6 = InterestPointHook()
    hook7 = TemplateCompareHook({"amazon": IMAGE_PATH})

    # --- cutter ---
    cutter = VideoCutter(compress_rate=0.9)
    # add hook
    cutter.add_hook(hook)
    cutter.add_hook(hook1)
    cutter.add_hook(hook2)
    cutter.add_hook(hook3)
    cutter.add_hook(hook4)
    cutter.add_hook(hook5)
    cutter.add_hook(hook6)
    cutter.add_hook(hook7)

    res = cutter.cut(VIDEO_PATH)
    stable, unstable = res.get_range()
    assert len(stable) == 2, "count of stable range is not correct"

    data_home = res.pick_and_save(stable, 5)
    assert os.path.isdir(data_home), "result dir not existed"

    # --- classify ---
    cl = SVMClassifier()
    cl.load(data_home)
    cl.train()
    classify_result = cl.classify(VIDEO_PATH, stable)

    # --- draw ---
    r = Reporter()
    report_path = os.path.join(data_home, "report.html")
    r.draw(classify_result, report_path=report_path, cut_result=res)
    assert os.path.isfile(report_path)

    # hook check
    assert os.path.isdir(frame_home)
    assert hook6.result
    assert hook7.result
