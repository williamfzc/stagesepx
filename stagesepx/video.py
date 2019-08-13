import os

from stagesepx import toolbox


class VideoObject(object):
    def __init__(self,
                 path: str = None,
                 *_, **__):
        assert os.path.isfile(path), f'video [{path}] not existed'
        self.path = path

        with toolbox.video_capture(path) as cap:
            self.frame_count = toolbox.get_frame_count(cap)
            self.frame_size = toolbox.get_frame_size(cap)

    def __str__(self):
        return f'<VideoObject path={self.path}>'

    __repr__ = __str__
