from stagesepx.cutter import VideoCutter
from stagesepx.classifier import SVMClassifier
from stagesepx.reporter import Reporter

import os

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
VIDEO_PATH = os.path.join(PROJECT_PATH, 'demo.mp4')
MODEL_PATH = os.path.join(PROJECT_PATH, 'model.pkl')


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
    cl = SVMClassifier()
    cl.load(data_home)
    cl.train()
    cl.save_model(MODEL_PATH)
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


def test_save_and_load():
    # test save and load
    cl = SVMClassifier()
    cl.load_model(MODEL_PATH)

    classify_result = cl.classify(VIDEO_PATH)

    # --- draw ---
    r = Reporter()
    r.draw(classify_result)
