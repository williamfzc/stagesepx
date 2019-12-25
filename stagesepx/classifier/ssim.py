from loguru import logger

from stagesepx.classifier.base import BaseClassifier
from stagesepx import toolbox
from stagesepx.video import VideoFrame


class SSIMClassifier(BaseClassifier):
    def _classify_frame(
        self, frame: VideoFrame, threshold: float = None, *_, **__
    ) -> str:
        if not threshold:
            threshold = 0.85

        result = list()
        for each_stage_name, each_stage_pic_list in self.read():
            each_result = list()
            for target_pic in each_stage_pic_list:
                # apply hooks
                target_pic = self._apply_hook(VideoFrame(-1, -1.0, target_pic))
                target_pic = target_pic.data

                each_pic_ssim = toolbox.compare_ssim(frame.data, target_pic)
                each_result.append(each_pic_ssim)
            ssim = max(each_result)
            result.append((each_stage_name, ssim))
            logger.debug(f"stage [{each_stage_name}]: {ssim}")

        result = max(result, key=lambda x: x[1])
        if result[1] < threshold:
            logger.debug("not a known stage, set it -1")
            result = ("-1", result[1])
        return result[0]
