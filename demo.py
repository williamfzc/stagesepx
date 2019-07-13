from stagesepx.cutter import VideoCutter
from stagesepx.classifier import SSIMClassifier
from stagesepx.reporter import Reporter


# cut
video_path = 'video/demo_video.mp4'
cutter = VideoCutter(period=4)
res = cutter.cut(video_path)
stable = res.get_stable_range()
data_home = res.pick_and_save(stable, 3)

# classify
cl = SSIMClassifier()
cl.load(data_home)
res = cl.classify(video_path)

# draw
Reporter.draw(res)
