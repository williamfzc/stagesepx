import os
import tempfile

from stagesepx.api import analyse, run

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
VIDEO_PATH = os.path.join(PROJECT_PATH, "demo.mp4")


def test_analyse():
    with tempfile.NamedTemporaryFile(suffix=".html", mode="w") as f:
        analyse(VIDEO_PATH, f.name)


def test_run():
    config = {
        # fmt: off
        "video": {
            "path": VIDEO_PATH,
        },
        "output": ".",
    }
    run(config)
