import os

from stagesepx import toolbox


class VideoObject(object):
    def __init__(self, video_path: str):
        assert os.path.isfile(video_path), f'video [{video_path}] not existed'
        self.path = video_path

        with toolbox.video_capture(video_path) as cap:
            self.frame_count = toolbox.get_frame_count(cap)
            self.frame_size = toolbox.get_frame_size(cap)

    def __str__(self):
        return f'<VideoObject path={self.path}>'

    __repr__ = __str__
