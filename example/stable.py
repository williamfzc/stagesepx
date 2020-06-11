from stagesepx.cutter import VideoCutter
from stagesepx.classifier import SVMClassifier
from stagesepx.reporter import Reporter
from stagesepx.video import VideoObject
import os

video = "../demo.mp4"

video = VideoObject(
    video,
    # 预加载，大幅度提升分析速度
    pre_load=True,
)

# --- cut ---
cutter = VideoCutter()

# 开始切割
res = cutter.cut(video)

# 你可以通过res获取切割结果，获取稳定状态与活动状态分别对应的区间
stable, unstable = res.get_range(
    # 判定阶段是否稳定的阈值
    # 越高则越严格（判定为稳定的区间更少）
    # 默认为 0.95 （0-1）
    threshold=0.95,
    # offset主要用于弥补 在变化过程中 有一些变化不大的相邻帧 被判定为稳态 导致连续变化过程被切割成多个部分 的情况
    # 可以参考 https://github.com/williamfzc/stagesepx/issues/16#issuecomment-517916995
    # 在上面的例子中，165 - 174 是一个变化过程，而因为 166 - 167 的变化不大导致整个过程被切断
    # 如果将offset设置为2，stagesepx会自动拟合在变化过程中长度小于等于2的稳定区间，使变化过程能够完整呈现
    offset=None,
)

# 对区间进行采样
# 采样出来的图片将保存原始尺寸以便后续分析，但会成为灰度图
data_home = res.pick_and_save(
    # 这里的例子是对稳定区间进行采样
    stable,
    # 每段区间的采样数，5即每个阶段等距离截取5张图片
    # 如果涉及机器学习，建议将此值提高
    5,
)

# --- classify ---
cl = SVMClassifier()

# 加载数据
cl.load(data_home)
# 在加载数据完成之后需要先训练
cl.train()

# 注意，如果在classify方法指定了范围
# 那么分析时只会分析处于范围内的帧！
# 例如，这里只传入了stable的范围，那么非stable范围内的帧都会被忽略掉，标记为 -1
classify_result = cl.classify(video, stable)

# 分类得到的结果是一个 ClassifierResult 对象
# 你可以直接通过处理里面的数据、使用它的内置方法对你的分类结果进行定制
# 从而达到你希望的效果
data_list = classify_result.data
print(data_list)
# classify_result 已经提供了许多方法用于更好地重整数据
# 可以直接进入 ClassifyResult 对象中查看
cr_dict = classify_result.to_dict()
print(cr_dict)

# --- draw ---
r = Reporter()

r.draw(
    classify_result,
    report_path=os.path.join(data_home, "report.html"),
    # 传入 unstable 可以将对应部分标记为 unstable
    # 会影响最终的分析结果
    unstable_ranges=unstable,
    # 0.5.3新增的特性，多用于debug
    # 传入cutter的切割结果，能够在图表末尾追加 SSIM、MSE、PSNR 的变化趋势图
    cut_result=res,
)
