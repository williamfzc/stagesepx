import os
import tempfile
from pydantic import ValidationError

from stagesepx.api import analyse, run, keras_train

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
VIDEO_PATH = os.path.join(PROJECT_PATH, "demo.mp4")


def test_analyse():
    with tempfile.NamedTemporaryFile(suffix=".html", mode="w") as f:
        analyse(VIDEO_PATH, f.name)


def test_train():
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
    # again (for coverage)
    keras_train(trainset, model_path=mod, epochs=1)

    # todo: weird. it did not work in github actions
    # predict with existed mod
    # config = {
    #     # fmt: off
    #     "video": {
    #         "path": VIDEO_PATH,
    #     },
    #     "classifier": {
    #         "classifier_type": "keras",
    #         "model": mod,
    #     },
    #     "output": ".",
    # }
    # run(config)


def test_run_validation():
    # enum
    config = {
        # fmt: off
        "video": {
            "path": VIDEO_PATH,
        },
        "classifier": {
            "classifier_type": "unknwonwonn",
        },
        "output": ".",
    }
    try:
        run(config)
    except ValidationError:
        pass
    else:
        raise TypeError("should raise an error if classifier_type is unexpected")

    config = {
        # fmt: off
        "video": {
            "path": VIDEO_PATH,
        },
        "output": ".",
        "calc": {
            "output": "some1.json",
            "operators": [
                {
                    "name": "error_test",
                    "calc_type": "unknwonww",
                },
            ]
        }
    }
    try:
        run(config)
    except ValidationError:
        pass
    else:
        raise TypeError("should raise an error if calc_type is unexpected")


def test_run_calc():
    config = {
        # fmt: off
        "video": {
            "path": VIDEO_PATH,
        },
        "output": ".",
        "calc": {
            "output": "some1.json",
            "operators": [
                {
                    "name": "calc_between_0_1",
                    "calc_type": "between",
                    "args": {
                        "from_stage": "0",
                        "to_stage": "1",
                    },
                },
                {
                    "name": "display everything",
                    "calc_type": "display",
                }
            ]
        }
    }
    run(config)
