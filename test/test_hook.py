from stagesepx.cutter import VideoCutter
from stagesepx.classifier import SVMClassifier
from stagesepx.reporter import Reporter
from stagesepx.hook import ExampleHook, IgnoreHook, CropHook, FrameSaveHook

import os

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
VIDEO_PATH = os.path.join(PROJECT_PATH, 'demo.mp4')


def test_hook():
    # init hook
    hook = ExampleHook()
    hook1 = ExampleHook(overwrite=True)
    hook2 = IgnoreHook(
        size=(0.5, 0.5),
        overwrite=True
    )
    frame_home = os.path.join(PROJECT_PATH, 'frame_save_dir')
    hook3 = FrameSaveHook(frame_home)
    hook4 = CropHook(
        size=(0.5, 0.5),
        offset=(0., 0.5),
        overwrite=True,
    )

    # --- cutter ---
    cutter = VideoCutter()
    # add hook
    cutter.add_hook(hook)
    cutter.add_hook(hook1)
    cutter.add_hook(hook2)
    cutter.add_hook(hook3)
    cutter.add_hook(hook4)

    res = cutter.cut(VIDEO_PATH)
    stable, unstable = res.get_range()
    assert len(stable) == 2, 'count of stable range is not correct'

    data_home = res.pick_and_save(
        stable,
        5,
    )
    assert os.path.isdir(data_home), 'result dir not existed'

    # --- classify ---
    cl = SVMClassifier()
    cl.load(data_home)
    cl.train()
    classify_result = cl.classify(VIDEO_PATH, stable)

    # --- draw ---
    r = Reporter()
    report_path = os.path.join(data_home, 'report.html')
    r.draw(
        classify_result,
        report_path=report_path,
        cut_result=res,
    )
    assert os.path.isfile(report_path)

    # hook check
    assert os.path.isdir(frame_home)
