from stagesepx.classifier import SSIMClassifier, SVMClassifier
from stagesepx.reporter import Reporter
from stagesepx.cutter import VideoCutResult

from test_cutter import test_default as cutter_default
from test_cutter import RESULT_DIR as CUTTER_RESULT_DIR

import os

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
VIDEO_PATH = os.path.join(PROJECT_PATH, "demo.mp4")
MODEL_PATH = os.path.join(PROJECT_PATH, "model.pkl")

# cut, and get result dir
cutter_res: VideoCutResult = cutter_default()


def _draw_report(res):
    r = Reporter()
    report_path = os.path.join(CUTTER_RESULT_DIR, "report.html")
    r.draw(res, report_path=report_path)
    assert os.path.isfile(report_path)


def test_default():
    # --- classify ---
    cl = SVMClassifier()
    cl.load(CUTTER_RESULT_DIR)
    cl.train()
    cl.save_model(MODEL_PATH, overwrite=True)
    classify_result = cl.classify(VIDEO_PATH)

    # --- draw ---
    _draw_report(classify_result)


def test_ssim_classifier():
    cl = SSIMClassifier()
    cl.load(CUTTER_RESULT_DIR)
    classify_result = cl.classify(VIDEO_PATH)

    # --- draw ---
    _draw_report(classify_result)


def test_work_with_cutter():
    cl = SVMClassifier()
    cl.load_model(MODEL_PATH)
    stable, _ = cutter_res.get_range()
    classify_result = cl.classify(VIDEO_PATH, stable)

    # --- draw ---
    _draw_report(classify_result)


def test_save_and_load():
    cl = SVMClassifier()
    cl.load_model(MODEL_PATH)
    classify_result = cl.classify(VIDEO_PATH)

    result_file = "save.json"
    reporter = Reporter()
    reporter.save(result_file, classify_result)
    assert os.path.isfile(result_file)
    classify_result_after = Reporter.load(result_file)

    assert len(classify_result) == len(classify_result_after)
    for i, j in zip(classify_result, classify_result_after):
        assert i.to_dict() == j.to_dict()
