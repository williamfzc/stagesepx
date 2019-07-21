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
    '../test.mp4',
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
Reporter.draw(
    res,
    report_path='report.html',
    # 在结果报告中展示stage对应的图片
    data_path=data_home,
)
