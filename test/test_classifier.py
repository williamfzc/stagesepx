from stagesepx.classifier import SSIMClassifier, SVMClassifier
from stagesepx.classifier.keras import KerasClassifier
from stagesepx.classifier.base import ClassifierResult
from stagesepx.reporter import Reporter
from stagesepx.cutter import VideoCutResult
from stagesepx import toolbox
import numpy as np

from test_cutter import test_default as cutter_default
from test_cutter import RESULT_DIR as CUTTER_RESULT_DIR

import os

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
VIDEO_PATH = os.path.join(PROJECT_PATH, "demo.mp4")
MODEL_PATH = os.path.join(PROJECT_PATH, "model.pkl")
IMAGE_NAME = "demo.jpg"
IMAGE_PATH = os.path.join(PROJECT_PATH, IMAGE_NAME)

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
    cl.classify(VIDEO_PATH, boost_mode=False)


def test_ssim_classifier():
    cl = SSIMClassifier()
    cl.load(CUTTER_RESULT_DIR)
    cl.classify(VIDEO_PATH, boost_mode=False)


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
    classify_result = cl.classify(VIDEO_PATH, boost_mode=False)

    result_file = "save.json"
    reporter = Reporter()
    reporter.add_extra("some_name", "some_value")
    reporter.save(result_file, classify_result)
    assert os.path.isfile(result_file)
    classify_result_after = Reporter.load(result_file)

    assert classify_result.get_length() == classify_result_after.get_length()
    for i, j in zip(classify_result.data, classify_result_after.data):
        assert i.to_dict() == j.to_dict()

    assert isinstance(reporter.get_stable_stage_sample(classify_result), np.ndarray)


def test_keep_data():
    cl = SVMClassifier()
    cl.load_model(MODEL_PATH)
    stable, _ = cutter_res.get_range()
    classify_result = cl.classify(VIDEO_PATH, stable, keep_data=True)

    # todo findit bug here
    image_object = toolbox.imread(IMAGE_PATH)[0:20, 0:20]
    assert classify_result.data[0].contain_image(image_object=image_object)


def test_result():
    cl = SVMClassifier()
    cl.load_model(MODEL_PATH)
    stable, _ = cutter_res.get_range()
    classify_result = cl.classify(VIDEO_PATH, stable, keep_data=True)

    assert classify_result.to_dict()
    classify_result.mark_range(1, 3, "0")
    classify_result.mark_range_unstable(1, 3)
    classify_result.get_important_frame_list()
    classify_result.get_stage_range()
    classify_result.get_specific_stage_range("0")
    classify_result.get_not_stable_stage_range()
    classify_result.mark_range_ignore(23, 24)
    classify_result.time_cost_between("0", "1")
    assert classify_result.contain("1")
    assert classify_result.first("1").frame_id == 20
    assert classify_result.last("1").frame_id == 21
    assert classify_result.is_order_correct(["0", "0", "1", "2"])
    assert classify_result.is_order_correct(["0", "0", "2"])
    assert classify_result.is_order_correct(["0", "1"])
    assert classify_result.is_order_correct(["0", "2"])
    assert classify_result.is_order_correct(["1", "2"])


def test_dump_and_load():
    cl = SVMClassifier()
    cl.load_model(MODEL_PATH)
    classify_result = cl.classify(VIDEO_PATH, boost_mode=False)

    json_path = "classify_result.json"
    classify_result.dump(json_path)

    res_from_file = ClassifierResult.load(json_path)
    assert classify_result.dumps() == res_from_file.dumps()

    # test diff
    assert classify_result.diff(res_from_file).ok()

    diffobj = classify_result.diff(res_from_file)
    diffobj.get_diff_str()


def test_keras():
    # set epochs to 1 for quickly training (test only)
    cl = KerasClassifier(epochs=1)
    cl.train(CUTTER_RESULT_DIR)
    cl.save_model("haha.h5")
    # recreate
    cl = KerasClassifier()
    cl.load_model("haha.h5")
    stable, _ = cutter_res.get_range()
    classify_result = cl.classify(VIDEO_PATH, stable, keep_data=True)
    assert classify_result.to_dict()
    # not stable in case
    assert cl.predict(IMAGE_PATH) in ("0", "1", "2")
