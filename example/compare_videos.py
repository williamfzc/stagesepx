from stagesepx.cutter import VideoCutter

import pprint

video_path = '../test1.mp4'
another_video_path = '../test2.mp4'

cutter = VideoCutter()
res = cutter.cut(video_path, compress_rate=0.1)
res1 = cutter.cut(another_video_path, compress_rate=0.1)

# version >= 0.4.3
pprint.pprint(
    res.diff(res1, frame_count=3)
)
