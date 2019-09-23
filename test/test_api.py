import os

from stagesepx.api import cut, classify, one_step
from stagesepx.reporter import Reporter

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
VIDEO_PATH = os.path.join(PROJECT_PATH, 'demo.mp4')


def test_one_step():
    one_step(VIDEO_PATH)


def test_cut_and_classify():
    # --- cutter ---
    res, data_home = cut(VIDEO_PATH)

    # --- classify ---
    classify_result = classify(VIDEO_PATH, data_home)

    # --- draw ---
    r = Reporter()
    r.draw(
        classify_result,
        report_path=os.path.join(data_home, "report.html"),
        cut_result=res,
    )
