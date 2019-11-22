"""
这是一个最小化的 stagesepx 使用例子
每一行的注释均可以在 cut_and_classify.py 中找到
"""
from stagesepx.cutter import VideoCutter
from stagesepx.classifier import SVMClassifier
from stagesepx.reporter import Reporter
from stagesepx.video import VideoObject

video_path = "../demo.mp4"
video = VideoObject(video_path)
video.load_frames()

# --- cutter ---
cutter = VideoCutter()
res = cutter.cut(video)
stable, unstable = res.get_range()
data_home = res.pick_and_save(stable, 5)

# --- classify ---
cl = SVMClassifier()
cl.load(data_home)
cl.train()
classify_result = cl.classify(video, stable)

# --- draw ---
r = Reporter()
r.draw(classify_result)
