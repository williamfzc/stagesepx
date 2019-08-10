from loguru import logger
import cv2
import numpy as np

from stagesepx.classifier.base import BaseClassifier
from stagesepx import toolbox


class SSIMClassifier(BaseClassifier):
    def _classify_frame(self,
                        frame_id: int,
                        frame: np.ndarray,
                        video_cap: cv2.VideoCapture,
                        threshold: float = None,
                        *_, **__) -> str:
        if not threshold:
            threshold = 0.85

        frame = toolbox.compress_frame(
            frame,
            self.compress_rate,
            self.target_size,
        )

        result = list()
        for each_stage_name, each_stage_pic_list in self.read(video_cap):
            each_result = list()
            for target_pic in each_stage_pic_list:
                target_pic = toolbox.compress_frame(target_pic, self.compress_rate, self.target_size)
                each_pic_ssim = toolbox.compare_ssim(frame, target_pic)
                each_result.append(each_pic_ssim)
            ssim = max(each_result)
            result.append((each_stage_name, ssim))
            logger.debug(f'stage [{each_stage_name}]: {ssim}')

        result = max(result, key=lambda x: x[1])
        if result[1] < threshold:
            logger.debug('not a known stage, set it -1')
            result = ('-1', result[1])
        return result[0]
