import pathlib
import typing
import cv2
from loguru import logger

from stagesepx import toolbox


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


class _BaseClassifier(object):
    pass


class SSIMClassifier(_BaseClassifier):
    def __init__(self):
        self.data: typing.Dict[str, typing.List[pathlib.Path]] = dict()

    def load(self, data_home: str):
        p = pathlib.Path(data_home)
        stage_dir_list = p.iterdir()
        for each in stage_dir_list:
            stage_name = each.name
            stage_pic_list = [i.absolute() for i in each.iterdir()]
            self.data[stage_name] = stage_pic_list
            logger.debug(f'stage [{stage_name}] found, and got {len(stage_pic_list)} pics')

    def classify(self, video_path: str) -> typing.List[ClassifierResult]:
        assert self.data, 'should load data first'

        final_result: typing.List[ClassifierResult] = list()
        with toolbox.video_capture(video_path) as cap:
            ret, frame = cap.read()
            while ret:
                frame_id = toolbox.get_current_frame_id(cap)
                frame_timestamp = toolbox.get_current_frame_time(cap)
                frame = toolbox.compress_frame(frame)

                result = list()
                for each_stage_name, each_stage_pic_list in self.data.items():
                    target_pic = cv2.imread(each_stage_pic_list[0].as_posix())
                    target_pic = toolbox.compress_frame(target_pic)

                    ssim = toolbox.compare_ssim(frame, target_pic)
                    result.append((each_stage_name, ssim))
                    logger.debug(f'stage [{each_stage_name}]: {ssim}')

                result = max(result, key=lambda x: x[1])
                logger.info(f'frame {frame_id} ({frame_timestamp}) belongs to {result[0]}')

                final_result.append(ClassifierResult(video_path, frame_id, frame_timestamp, result[0]))
                ret, frame = cap.read()
        return final_result


if __name__ == '__main__':
    s = SSIMClassifier()
    s.load('../1562999463')
    res = s.classify('../video/demo_video.mp4')

