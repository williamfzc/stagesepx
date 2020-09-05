import os
import tempfile

from stagesepx.api import analyse, run, keras_train

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
VIDEO_PATH = os.path.join(PROJECT_PATH, "demo.mp4")


def test_analyse():
    with tempfile.NamedTemporaryFile(suffix=".html", mode="w") as f:
        analyse(VIDEO_PATH, f.name)


def test_run():
    trainset = os.path.join(PROJECT_PATH, "trainset")
    mod = os.path.join(PROJECT_PATH, "a.mod")
    config = {
        # fmt: off
        "video": {
            "path": VIDEO_PATH,
        },
        "output": ".",
        "extras": {
            "save_train_set": trainset,
        }
    }
    run(config)

    # train
    keras_train(trainset, model_path=mod, epochs=1)

    # predict with existed mod
    config = {
        # fmt: off
        "video": {
            "path": VIDEO_PATH,
        },
        "classifier": {
            "classifier_type": "keras",
            "model": mod,
        },
        "output": ".",
        "extras": {
            "save_train_set": trainset,
        }
    }
    run(config)
