from stagesepx.cutter import VideoCutter, VideoCutResult
from stagesepx.classifier import SVMClassifier
from stagesepx.reporter import Reporter
from stagesepx.hook import ExampleHook
import os


video_path = '../demo.mp4'

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

# 在 0.4.2 之后，hook特性正式被加入：https://williamfzc.github.io/stagesepx/#/pages/3_how_it_works?id=hook
# 使用极其简单，你只需要初始化 hook
hook = ExampleHook()
# 再将 hook 添加到 cutter 或者 classifier 中去
cutter.add_hook(hook)
# 支持多个hook，他们会按顺序执行
# 当 overwrite 被设置为 true 时，hook的修改将会持续影响到后续的分析
# 否则 hook 操作的都是 frame 的副本
hook1 = ExampleHook(overwrite=True)
cutter.add_hook(hook1)

# 开始切割
res = cutter.cut(
    video_path,
    # block 能够对每帧进行切割并分别进行比较，计算出更加敏感的ssim值
    # 默认为2，即切为4宫格；若为4，即切为16宫格，以此类推；为1即不做切割，全图比较
    # 值得注意，如果无法整除，block是会报错的
    block=2,
)

# 你可以将你的cutter结果保存起来，供其他时刻使用（>=0.4.4）
cut_result = res.dumps()
# 或直接保存成json文件
# res.dump('./YOUR_RES.json')
# 在你想要使用时，使用loads读取即可
res = VideoCutResult.loads(cut_result)
# 或直接从文件读取
# res = VideoCutResult.load('./YOUR_RES.json')

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
    psnr_threshold=None,
    # limit 能够过滤掉一些过于短的阶段（你可以用它忽略一些持续时间较短的变化），默认不过滤
    # 例如填入5，持续区间短于 5*step 的会被忽略
    limit=None,
    # offset主要用于弥补 在变化过程中 有一些变化不大的相邻帧 被判定为稳态 导致连续变化过程被切割成多个部分 的情况
    # 可以参考 https://github.com/williamfzc/stagesepx/issues/16#issuecomment-517916995
    # 在上面的例子中，165 - 174 是一个变化过程，而因为 166 - 167 的变化不大导致整个过程被切断
    # 如果将offset设置为2，stagesepx会自动拟合在变化过程中长度小于等于2的稳定区间，使变化过程能够完整呈现
    offset=None,
)

# 你可以通过 thumbnail 将阶段的变化过程转化成一张缩略图，这样可以很直观地看出阶段的变化过程！
# 例如，你希望查看第一个unstable阶段发生了什么
# 这样做能够将转化后的缩略图保存到当前目录下
# res.thumbnail(unstable[0], to_dir='.')

# 对区间进行采样
# 采样出来的图片将保存原始尺寸以便后续分析，但会成为灰度图
data_home = res.pick_and_save(
    # 这里的例子是对稳定区间进行采样
    stable,
    # 每段区间的采样数，5即每个阶段等距离截取5张图片
    # 如果涉及机器学习，建议将此值提高
    5,
    # 采样结果保存的位置
    # 不指定的话则会在当前位置生成文件夹并返回它的路径
    # './cut_result',

    # prune被用于去除重复阶段（>=0.4.4）
    # float（0-1.0），设置为0.9时，如果两个stage相似度超过0.9，他们会合并成一个类别
    prune=None,
)

# --- classify ---

cl = SVMClassifier(
    # 默认情况下使用 HoG 进行特征提取
    # 你可以将其关闭从而直接对原始图片进行训练与测试：feature_type='raw'
    feature_type='hog',
    # 默认为0.2，即将图片缩放为0.2倍
    # 主要为了提高计算效率
    # 如果你担心影响分析效果，可以将其提高
    compress_rate=0.2,
)

# 加载数据
cl.load(data_home)
# 在加载数据完成之后需要先训练
cl.train()
# 在训练后你可以把模型保存起来
# cl.save_model('model.pkl')
# 或者直接读取已经训练好的模型
# cl.load_model('model.pkl')

# 注意，如果在classify方法指定了范围
# 那么分析时只会分析处于范围内的帧！
# 例如，这里只传入了stable的范围，那么非stable范围内的帧都会被忽略掉，标记为 -1
classify_result = cl.classify(
    video_path,
    stable,
    # 步长，可以自行设置用于平衡效率与颗粒度
    # 默认为1，即每帧都检测
    step=1,
)

# 分类出来的结果是一个 list，里面包含 ClassifierResult 对象
# 你可以用它进行二次开发
for each in classify_result:
    # 它的帧编号
    print(each.frame_id)
    # 它的时间戳
    print(each.timestamp)
    # 它被划分为什么类型
    print(each.stage)
    break

# --- draw ---
r = Reporter()

# 你可以将 thumbnail 直接嵌入到report中
# 如果不手动设定的话，report也会在报告中自动加入 thumbnail
# 但如此做，你需要在 draw函数 传入 与你的 get_range 相同的参数
# 否则自动提取的阶段会采用默认参数，可能会与你希望的不太一样
# 可以参考 cli.py 中的实现
for each in unstable:
    r.add_thumbnail(
        f'{each.start}({each.start_time}) - {each.end}({each.end_time}), '
        f'duration: {each.end_time - each.start_time}',
        res.thumbnail(each)
    )

# 你可以将把一些文件夹路径插入到报告中
# 这样你可以很方便地从报告中查看各项相关内容
# 当然，你需要想好这些路径与报告最后所在位置之间的相对位置，以确保他们能够被访问到
# r.add_dir_link(data_home)

# 在0.3.2及之后的版本，你可以在报告中加入一些自定义内容 （https://github.com/williamfzc/stagesepx/issues/13）
# r.add_extra('here is title', 'here is content')
r.draw(
    classify_result,
    report_path=os.path.join(data_home, 'report.html'),
    # 0.5.3新增的特性，多用于debug
    # 传入cutter的切割结果，能够在图表末尾追加 SSIM、MSE、PSNR 的变化趋势图
    cut_result=res,
)
