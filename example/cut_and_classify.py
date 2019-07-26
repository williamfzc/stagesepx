from stagesepx.cutter import VideoCutter
from stagesepx.classifier import SVMClassifier
from stagesepx.reporter import Reporter

# cut
video_path = '../file4.mp4'
cutter = VideoCutter()
res = cutter.cut(video_path)
stable, unstable = res.get_range()
data_home = res.pick_and_save(stable, 5)

# classify
cl = SVMClassifier()
cl.load(data_home)
cl.train()

# 注意，如果在classify方法指定了范围
# 那么分析时只会分析处于范围内的帧！
# 例如，这里只传入了stable的范围，那么非stable范围内的帧都会被忽略掉，标记为 -1
classify_result = cl.classify(
    video_path,
    stable,
    # 步长，可以自行设置用于平衡效率与颗粒度
    # 默认为1，即每帧都检测
    step=1
)

# draw
r = Reporter()
r.add_dir_link(data_home)

# 你可以将 thumbnail 直接嵌入到report中
for each in unstable:
    r.add_thumbnail(f'{each.start}-{each.end}', res.thumbnail(each))

r.draw(classify_result)
