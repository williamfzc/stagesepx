from stagesepx.cutter import VideoCutter
from stagesepx.classifier import SSIMClassifier
from stagesepx.reporter import Reporter

# cut
video_path = '../demo.mp4'
cutter = VideoCutter()
res = cutter.cut(video_path)
stable = res.get_stable_range()

# classify
cl = SSIMClassifier()
cl.load(stable)

res = cl.classify(
    video_path,
    stable,
)

# draw
r = Reporter()
r.draw(res)
