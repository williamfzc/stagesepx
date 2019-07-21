from stagesepx.cutter import VideoCutter
from stagesepx.classifier import SVMClassifier
from stagesepx.reporter import Reporter

# cut
video_path = '../test.mp4'
cutter = VideoCutter(step=5)
res = cutter.cut(video_path)
stable = res.get_stable_range()
data_home = res.pick_and_save(stable, 3)
print(stable)

# classify
cl = SVMClassifier()
cl.load(data_home)
cl.train()

# 注意，如果在classify方法指定了范围
# 那么分析时只会分析处于范围内的帧！
# 例如，这里只传入了stable的范围，那么非stable范围内的帧都会被忽略掉，标记为 -1
res = cl.classify(video_path, stable, step=5)

# draw
Reporter.draw(
    res,
    report_path=f'{data_home}/report.html',
    data_path=data_home,
)
