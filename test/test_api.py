import os
import tempfile
from pydantic import ValidationError

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
        "extras": {
            "save_train_set": trainset,
        }
    }
    try:
        run(config)
    except ValidationError:
        pass
    else:
        raise TypeError("should raise an error if classifier_type is unexpected")

    # calc
    config = {
        # fmt: off
        "video": {
            "path": VIDEO_PATH,
        },
        "output": ".",
        "extras": {
            "save_train_set": trainset,
        },
        "calc": {
            "output": "some1.json",
            "operators": [
                {
                    "name": "calc_between_1_2",
                    "calc_type": "between",
                    "args": {
                        "from_stage": "1",
                        "to_stage": "2",
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

    # train
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
