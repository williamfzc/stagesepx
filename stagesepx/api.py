"""
high level API
"""
import os
import typing
import traceback
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

    class _VideoUserConfig(BaseModel):
        path: str
        pre_load: bool = True
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

    class _CalcOperatorType(Enum):
        BETWEEN = "between"
        DISPLAY = "display"

    class _CalcOperator(BaseModel):
        name: str
        calc_type: _CalcOperatorType
        args: dict = dict()

    class _CalcUserConfig(BaseModel):
        output: str = None
        ignore_error: bool = None
        operators: typing.List[_CalcOperator] = None

    class _ExtraUserConfig(BaseModel):
        save_train_set: str = None

    class UserConfig(BaseModel):
        output: str
        video: _VideoUserConfig
        cutter: _CutterUserConfig = _CutterUserConfig()
        classifier: _ClassifierUserConfig = _ClassifierUserConfig()
        calc: _CalcUserConfig = _CalcUserConfig()
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
        fps=config.video.fps,
    )
    if config.video.pre_load:
        video.load_frames()

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
        # validation has been applied by pydantic
        # so no `else`

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

    # calc
    def _calc_display() -> dict:
        # jsonify
        return json.loads(classify_result.dumps())

    def _calc_between(*, from_stage: str = None, to_stage: str = None) -> dict:
        assert classify_result.contain(
            from_stage
        ), f"no stage {from_stage} found in result"
        assert classify_result.contain(to_stage), f"no stage {to_stage} found in result"
        from_frame = classify_result.last(from_stage)
        to_frame = classify_result.first(to_stage)
        cost = to_frame.timestamp - from_frame.timestamp
        return {
            "from": from_frame.frame_id,
            "to": to_frame.frame_id,
            "cost": cost,
        }

    _calc_func_dict = {
        _CalcOperatorType.BETWEEN: _calc_between,
        _CalcOperatorType.DISPLAY: _calc_display,
    }
    calc_output = config.calc.output
    if calc_output:
        output_path = pathlib.Path(calc_output)
        assert not output_path.is_file(), f"file {output_path} already existed"
        result = []
        for each_calc in config.calc.operators:
            func = _calc_func_dict[each_calc.calc_type]
            try:
                func_ret = func(**each_calc.args)
            except Exception as e:
                if not config.calc.ignore_error:
                    raise
                logger.warning(e)
                func_ret = traceback.format_exc()
            calc_ret = {
                "name": each_calc.name,
                "type": each_calc.calc_type.value,
                "result": func_ret,
            }
            result.append(calc_ret)
        with open(output_path, "w", encoding=constants.CHARSET) as f:
            json.dump(result, f)

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

    assert not os.path.isfile(model_path), f"file {model_path} already existed"
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
