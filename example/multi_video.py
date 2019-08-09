from stagesepx.cutter import VideoCutter
from stagesepx.classifier import SVMClassifier
from stagesepx.reporter import Reporter

video_list = [
    '../demo.mp4',
    # 把别的视频也配置在这里即可
]

for each_video_path in video_list:
    cutter = VideoCutter()
    res = cutter.cut(each_video_path)
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
    res = cl.classify(
        each_video_path,
        stable,
        # 步长，可以自行设置用于平衡效率与颗粒度
        # 默认为1，即每帧都检测
        step=1
    )

    # 为了更方便的可读性，stagesepx已经内置了图表绘制功能
    # 你可以直接把分析结果绘制成图表
    report = Reporter()
    # 你可以将把一些文件夹路径插入到报告中
    # 这样你可以很方便地从报告中查看各项相关内容
    # 当然，你需要想好这些路径与报告最后所在位置之间的相对位置，以确保他们能够被访问到
    report.add_dir_link(data_home)

    report.draw(res)
