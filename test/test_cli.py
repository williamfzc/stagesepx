from loguru import logger
import subprocess
import os
import shutil

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
VIDEO_PATH = os.path.join(PROJECT_PATH, "demo.mp4")


def test_cli():
    logger.info("checking main")
    subprocess.check_call(["python", "-m", "stagesepx.cli"])

    logger.info("checking keras trainer ...")
    subprocess.check_call(["stagesepx", "train", "output", "output.h5"])
    # try to train
    subprocess.check_call(
        ["stagesepx", "train", "output", "output.h5", "--epochs", "1"]
    )

    subprocess.check_call(["stagesepx", "analyse", VIDEO_PATH, "output"])
    shutil.rmtree("output")


def test_with_config():
    subprocess.check_call(["stagesepx", "run", "test/min_run_config.json"])
    subprocess.check_call(["stagesepx", "run", "test/run_config.json"])
