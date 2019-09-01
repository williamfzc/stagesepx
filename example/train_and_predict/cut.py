"""
这个例子描述了如何采集训练集
"""
from stagesepx.cutter import VideoCutter


video_path = '../../demo.mp4'

# --- cut ---
cutter = VideoCutter(
    # 步长，默认为1，通过它可以自行把握效率与颗粒度
    # 设定为2时，会以2帧为一个单位进行遍历
    # 即跳过一帧
    step=1,
    # 默认为0.2，即将图片缩放为0.2倍
    # 主要为了提高计算效率
    # 如果你担心影响分析效果，可以将其提高
    compress_rate=0.2,
    # 或者直接指定尺寸
    # 当压缩率与指定尺寸同时传入时，优先以指定尺寸为准
    # target_size=(200, 400),
)

# 开始切割
res = cutter.cut(
    video_path,
    # block 能够对每帧进行切割并分别进行比较，计算出更加敏感的ssim值
    # 默认为2，即切为4宫格；若为4，即切为16宫格，以此类推；为1即不做切割，全图比较
    # 值得注意，如果无法整除，block是会报错的
    block=2,
)

# 你可以通过res获取切割结果，获取稳定状态与活动状态分别对应的区间
stable, unstable = res.get_range(
    # 判定阶段是否稳定的阈值
    # 越高则越严格（判定为稳定的区间更少）
    # 默认为 0.95 （0-1）
    threshold=0.95,
    # 利用 psnr 进行增强型的检测
    # 0.5.3加入的特性，默认关闭（float，0-1）
    # 设定后，它将对被认为stable的区间进行二次检测
    # 例如，设定为0.5时，稳定区间的条件将变为：
    # ssim > 0.95 and psnr > 0.5
    # 详见 https://github.com/williamfzc/stagesepx/issues/38
    # psnr_threshold=0.5,
    # limit 能够过滤掉一些过于短的阶段（你可以用它忽略一些持续时间较短的变化），默认不过滤
    # 例如填入5，持续区间短于 5*step 的会被忽略
    limit=None,
    # offset主要用于弥补 在变化过程中 有一些变化不大的相邻帧 被判定为稳态 导致连续变化过程被切割成多个部分 的情况
    # 可以参考 https://github.com/williamfzc/stagesepx/issues/16#issuecomment-517916995
    # 在上面的例子中，165 - 174 是一个变化过程，而因为 166 - 167 的变化不大导致整个过程被切断
    # 如果将offset设置为2，stagesepx会自动拟合在变化过程中长度小于等于2的稳定区间，使变化过程能够完整呈现
    # offset=3,
)

# 对区间进行采样
# 采样出来的图片将保存原始尺寸以便后续分析，但会成为灰度图
res.pick_and_save(
    # 这里的例子是对稳定区间进行采样
    stable,
    # 每段区间的采样数，5即每个阶段等距离截取5张图片
    # 如果涉及机器学习，建议将此值提高
    5,
    # 采样结果保存的位置
    # 不指定的话则会在当前位置生成文件夹并返回它的路径
    './cut_result',

    # prune被用于去除重复阶段（>=0.4.4）
    # float（0-1.0），设置为0.9时，如果两个stage相似度超过0.9，他们会合并成一个类别
    prune=None,
)
