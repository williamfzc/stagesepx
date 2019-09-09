from stagesepx.cutter import VideoCutter
from stagesepx.classifier import SSIMClassifier
from stagesepx.reporter import Reporter

import os

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
VIDEO_PATH = os.path.join(PROJECT_PATH, 'demo.mp4')


def test_base():
    # --- cutter ---
    cutter = VideoCutter()
    res = cutter.cut(VIDEO_PATH)
    stable, unstable = res.get_range(limit=1)
    assert len(stable) == 3, 'count of stable range is not correct'

    data_home = res.pick_and_save(
        stable,
        5,
        prune=0.99,
    )
    assert os.path.isdir(data_home), 'result dir not existed'

    # --- classify ---
    cl = SSIMClassifier()
    cl.load(data_home)
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
