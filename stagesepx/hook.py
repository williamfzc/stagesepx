import numpy as np
import os
from loguru import logger
import cv2

from stagesepx import toolbox


class BaseHook(object):
    def __init__(self, *_, **__):
        # default: dict
        self.result = dict()

    def do(self, frame_id: int, frame: np.ndarray, *_, **__):
        raise NotImplementedError('MUST IMPLEMENT THIS FIRST')


class ExampleHook(BaseHook):
    def __init__(self):
        # you can handle result by yourself
        # change the type, or anything you want
        super().__init__()
        self.result = dict()

    def do(self, frame_id: int, frame: np.ndarray, *_, **__):
        frame = toolbox.turn_grey(frame)
        self.result[frame_id] = frame.shape


class FrameSaveHook(BaseHook):
    """ add this hook, and save all the frames you want to specific dir """
    def __init__(self, target_dir: str, *_, **__):
        super().__init__(*_, **__)

        self.target_dir = target_dir
        os.makedirs(target_dir, exist_ok=True)
        logger.debug(f'init frame saver, frames will be saved to {target_dir}')

    def do(self,
           frame_id: int,
           frame: np.ndarray,
           compress_rate: float = None,
           *args, **kwargs):
        if not compress_rate:
            compress_rate = 0.2

        compressed = toolbox.compress_frame(frame, compress_rate=compress_rate)
        target_path = os.path.join(self.target_dir, f'{frame_id}.png')
        cv2.imwrite(target_path, compressed)
