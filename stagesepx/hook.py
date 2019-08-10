import numpy as np
from stagesepx import toolbox


class BaseHook(object):
    name = 'hook'

    def __init__(self, *_, **__):
        # default: dict
        self.result = dict()

    def do(self, frame_id: int, frame: np.ndarray, *_, **__):
        raise NotImplementedError('MUST IMPLEMENT THIS FIRST')


class ExampleHook(BaseHook):
    name = 'example_hook'

    def __init__(self):
        super().__init__()
        self.result = dict()

    def do(self, frame_id: int, frame: np.ndarray, *_, **__):
        frame = toolbox.turn_grey(frame)
        self.result[frame_id] = frame.shape
