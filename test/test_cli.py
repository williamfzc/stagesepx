from loguru import logger
import subprocess
import os

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
VIDEO_PATH = os.path.join(PROJECT_PATH, "demo.mp4")

from test_cutter import test_default as cutter_default
from test_cutter import RESULT_DIR as CUTTER_RESULT_DIR

# prepare
cutter_default()


def test_cli():
    logger.info("checking main")
    subprocess.check_call(["python3", "-m", "stagesepx.cli"])


def test_analyse():
    output = "output.html"
    subprocess.check_call(["stagesepx", "analyse", VIDEO_PATH, output])
    os.remove(output)


def test_train():
    mod = "output.h5"
    subprocess.check_call(
        ["stagesepx", "train", CUTTER_RESULT_DIR, mod, "--epochs", "1"]
    )
    # predict
    subprocess.check_call(["stagesepx", "run", "test/run_config_with_model.json"])


def test_with_min_config():
    subprocess.check_call(["stagesepx", "run", "test/min_run_config.json"])


def test_with_fat_config():
    subprocess.check_call(["stagesepx", "run", "test/run_config.json"])
