from stagesepx.classifier import SSIMClassifier
from stagesepx.reporter import Reporter

# 在运行这个例子前需要有前置数据
# 你可以先从 cut.py 开始

# 这里用的分类器是默认的SSIM分类器
# 更多的分类器会在稳定之后逐步加入
cl = SSIMClassifier()
# cut.py会把数据生成在这个路径下
# 如果你改动了，这里也要做相应修改
data_home = './cut_result'
cl.load(data_home)
# 开始分析即可
res = cl.classify(
    '../demo.mp4',
    # 步长，可以自行设置用于平衡效率与颗粒度
    # 默认为1，即每帧都检测
    step=1
)

# 分类出来的结果是一个 list，里面包含 ClassifierResult 对象
# 你可以用它进行二次开发
for each in res:
    # 它的帧编号
    print(each.frame_id)
    # 它的时间戳
    print(each.timestamp)
    # 它被划分为什么类型
    print(each.stage)
    break

# 为了更方便的可读性，stagesepx已经内置了图表绘制功能
# 你可以直接把分析结果绘制成图表
report = Reporter()
# 你可以将把一些文件夹路径插入到报告中
# 这样你可以很方便地从报告中查看各项相关内容
# 当然，你需要想好这些路径与报告最后所在位置之间的相对位置，以确保他们能够被访问到
report.add_dir_link(data_home)

report.draw(
    res,
    report_path='report.html',
)
