import os
import tempfile
import uuid
from pydantic import ValidationError

from stagesepx.api import analyse, run, keras_train

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
VIDEO_PATH = os.path.join(PROJECT_PATH, "demo.mp4")


def _get_random_str():
    return str(uuid.uuid4())


def test_analyse():
    with tempfile.NamedTemporaryFile(suffix=".html", mode="w") as f:
        analyse(VIDEO_PATH, f.name)


def test_train():
    trainset = os.path.join(PROJECT_PATH, _get_random_str())
    mod = os.path.join(PROJECT_PATH, "a.h5")
    config = {
        # fmt: off
        "video": {
            "path": VIDEO_PATH,
            "fps": 30,
        },
        "output": ".",
        "extras": {
            "save_train_set": trainset,
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
            "output": f"{_get_random_str()}.json",
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

    config = {
        # fmt: off
        "video": {
            "path": VIDEO_PATH,
        },
        "output": ".",
        "calc": {
            "output": f"{_get_random_str()}.json",
            "ignore_error": True,
            "operators": [
                {
                    "name": "error_test",
                    "calc_type": "between",
                    "args": {
                        "from_stage": "0",
                        # unexpected stage
                        "to_stage": "999",
                    }
                },
            ]
        }
    }
    run(config)


def test_run_calc():
    config = {
        # fmt: off
        "video": {
            "path": VIDEO_PATH,
        },
        "output": ".",
        "calc": {
            "output": f"{_get_random_str()}.json",
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


def test_diff():
    from stagesepx.api import _diff

    diff_object = _diff(VIDEO_PATH, VIDEO_PATH)
    assert diff_object
    assert not diff_object.any_stage_lost()
    assert diff_object.stage_diff()
