from stagesepx.cutter import VideoCutter
from stagesepx.classifier import SVMClassifier

import pprint

video_path = '../0866.mp4'
another_video_path = '../0867.mp4'

cutter = VideoCutter()
res = cutter.cut(video_path, compress_rate=0.1)
res1 = cutter.cut(another_video_path, compress_rate=0.1)

stable, _ = res.get_range(limit=3)
stable1, _ = res1.get_range(limit=3)

data_path = res.pick_and_save(stable, 3)
data_path1 = res1.pick_and_save(stable1, 3)

cl = SVMClassifier()
cl1 = SVMClassifier()
cl.load(data_path)
cl1.load(data_path1)

pprint.pprint(cl.diff(cl1))
