"""
high level API
"""
import os
import typing
import uuid
import tempfile
import json
import pathlib
from enum import Enum
from loguru import logger
from pydantic import BaseModel

from stagesepx.cutter import VideoCutter
from stagesepx.classifier import SVMClassifier
from stagesepx.reporter import Reporter
from stagesepx import constants
from stagesepx.video import VideoObject


def run(config: typing.Union[dict, str]):
    """
    run with config

    :param config: config file path, or a preload dict
    :return:
    """

    class APIRuntimeError(RuntimeError):
        pass

    class _VideoUserConfig(BaseModel):
        path: str
        pre_load: bool = None
        fps: int = None

    class _CutterUserConfig(BaseModel):
        threshold: float = None
        frame_count: int = None
        offset: int = None
        limit: int = None
        block: int = None

        # common
        compress_rate: float = None
        target_size: typing.Tuple[int, int] = None

    class _ClassifierType(Enum):
        SVM = "svm"
        KERAS = "keras"

    class _ClassifierUserConfig(BaseModel):
        boost_mode: bool = None
        classifier_type: _ClassifierType = _ClassifierType.SVM
        model: str = None

        # common
        compress_rate: float = None
        target_size: typing.Tuple[int, int] = None

    class _ExtraUserConfig(BaseModel):
        save_train_set: str = None

    class UserConfig(BaseModel):
        output: str
        video: _VideoUserConfig
        cutter: _CutterUserConfig = _CutterUserConfig()
        classifier: _ClassifierUserConfig = _ClassifierUserConfig()
        extras: _ExtraUserConfig = _ExtraUserConfig()

    if isinstance(config, str):
        # path
        config_path = pathlib.Path(config)
        assert config_path.is_file(), f"no config file found in {config_path}"

        # todo: support different types in the future
        assert config_path.as_posix().endswith(
            ".json"
        ), "config file should be json format"
        with open(config_path, encoding=constants.CHARSET) as f:
            config = json.load(f)

    config = UserConfig(**config)
    logger.info(f"config: {config}")

    # main flow
    video = VideoObject(
        # fmt: off
        path=config.video.path,
        pre_load=config.video.pre_load,
        fps=config.video.fps,
    )

    # cut
    cutter = VideoCutter(
        # fmt: off
        compress_rate=config.cutter.compress_rate,
        target_size=config.cutter.target_size,
    )
    res = cutter.cut(
        # fmt: off
        video=video,
        block=config.cutter.block,
    )
    stable, unstable = res.get_range(
        # fmt: off
        threshold=config.cutter.threshold,
        offset=config.cutter.offset,
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        # classify
        if config.classifier.classifier_type is _ClassifierType.SVM:
            cl = SVMClassifier(
                # fmt: off
                compress_rate=config.classifier.compress_rate,
                target_size=config.classifier.target_size,
            )
        elif config.classifier.classifier_type is _ClassifierType.KERAS:
            from stagesepx.classifier.keras import KerasClassifier

            cl = KerasClassifier(
                # fmt: off
                compress_rate=config.classifier.compress_rate,
                target_size=config.classifier.target_size,
            )
        else:
            raise APIRuntimeError(
                f"classifier_type should be: {_ClassifierType.enum_members}"
            )

        if config.classifier.model:
            # no need to retrain
            model_path = pathlib.Path(config.classifier.model)
            assert model_path.is_file(), f"file {model_path} not existed"
            cl.load_model(model_path)
        else:
            # train a new model
            train_set_dir = config.extras.save_train_set or temp_dir
            os.makedirs(train_set_dir, exist_ok=True)

            res.pick_and_save(
                # fmt: off
                stable,
                frame_count=config.cutter.frame_count,
                to_dir=train_set_dir,
            )
            cl.train(data_path=train_set_dir)

    # start classifying
    classify_result = cl.classify(
        # fmt: off
        video,
        stable,
        boost_mode=config.classifier.boost_mode,
    )

    # draw
    r = Reporter()
    r.draw(
        # fmt: off
        classify_result,
        report_path=config.output,
    )


def keras_train(
    train_data_path: str,
    model_path: str,
    # options
    epochs: int = 10,
    target_size: str = "600x800",
    overwrite: bool = False,
    **kwargs,
):
    from stagesepx.classifier.keras import KerasClassifier

    # handle args
    target_size: typing.Sequence[int] = [int(each) for each in target_size.split("x")]

    cl = KerasClassifier(
        # 轮数
        epochs=epochs,
        # 保证数据集的分辨率统一性
        target_size=target_size,
        **kwargs,
    )
    cl.train(train_data_path)

    # file existed
    while os.path.isfile(model_path):
        logger.warning(f"file {model_path} already existed")
        model_path = f"{uuid.uuid4()}.h5"
        logger.debug(f"trying to save it to {model_path}")
    cl.save_model(model_path, overwrite=overwrite)


def analyse(
    video: typing.Union[str, VideoObject],
    output_path: str,
    pre_load: bool = True,
    threshold: float = 0.98,
    offset: int = 3,
    boost_mode: bool = True,
):
    """ designed for https://github.com/williamfzc/stagesepx/issues/123 """

    if isinstance(video, str):
        video = VideoObject(video, pre_load=pre_load)

    cutter = VideoCutter()
    res = cutter.cut(video)

    stable, unstable = res.get_range(threshold=threshold, offset=offset,)

    with tempfile.TemporaryDirectory() as temp_dir:
        res.pick_and_save(
            stable, 5, to_dir=temp_dir,
        )

        cl = SVMClassifier()
        cl.load(temp_dir)
        cl.train()
        classify_result = cl.classify(video, stable, boost_mode=boost_mode)

    r = Reporter()
    r.draw(
        classify_result,
        report_path=output_path,
        unstable_ranges=unstable,
        cut_result=res,
    )
