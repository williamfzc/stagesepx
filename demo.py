from stagesepx.cutter import VideoCutter
from stagesepx.toolbox import get_frame, video_capture

import cv2

video_path = 'video/demo_video.mp4'
c = VideoCutter(period=4)
res = c.cut(video_path)
stable = res.get_stable_range()
unstable = res.get_unstable_range()
res.pick_and_save(stable, 3)
