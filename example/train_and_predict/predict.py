"""
利用训练好的模型，建立长期的视频分析工作流

在 train.py 之后，你应该能得到一个 model.pkl 模型
"""

from stagesepx.classifier import SVMClassifier
from stagesepx.cutter import VideoCutter
from stagesepx.reporter import Reporter

TARGET_VIDEO = '../../demo.mp4'

# cut
# 这里依旧使用了 cut，主要目的还是为了可以比较好的处理变化中的过程
# 但这次我们不需要用到 pick_and_save，因为这次 classifier 不会使用 cutter 的数据
cutter = VideoCutter()
res = cutter.cut(TARGET_VIDEO)
stable, _ = res.get_range()

# classify
# 这里的参数需要保持与train.py一致，如果你有改动的话
cl = SVMClassifier()
cl.load_model('./model.pkl')

classify_result = cl.classify(
    TARGET_VIDEO,
    stable,
)

r = Reporter()
r.draw(
    classify_result,
    report_path='report.html',
    cut_result=res,
)
