import pathlib
import typing
from loguru import logger


class StageData(object):
    def __init__(self, name: str, pic_list: typing.List[str]):
        self.name = name
        self.pic_list = pic_list


class ClassifierResult(object):
    def __init__(self,
                 video_path: str,
                 frame_id: int,
                 timestamp: float,
                 stage: str):
        self.video_path = video_path
        self.frame_id = frame_id
        self.timestamp = timestamp
        self.stage = stage


class BaseClassifier(object):
    def __init__(self):
        self.data: typing.Dict[str, typing.List[pathlib.Path]] = dict()

    def load(self, data_home: str):
        p = pathlib.Path(data_home)
        stage_dir_list = p.iterdir()
        for each in stage_dir_list:
            # load dir only
            if each.is_file():
                continue
            stage_name = each.name
            stage_pic_list = [i.absolute() for i in each.iterdir()]
            self.data[stage_name] = stage_pic_list
            logger.debug(f'stage [{stage_name}] found, and got {len(stage_pic_list)} pics')
