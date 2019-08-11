from stagesepx.cutter import VideoCutter
from stagesepx.classifier import SVMClassifier
from stagesepx.reporter import Reporter
from stagesepx.hook import ExampleHook


video_path = '../demo.mp4'

# --- cut ---
cutter = VideoCutter(
    # 步长，默认为1，通过它可以自行把握效率与颗粒度
    # 设定为2时，会以2帧为一个单位进行遍历
    # 即跳过一帧
    step=1,
)

# 在 0.4.2 之后，hook特性正式被加入：https://github.com/williamfzc/stagesepx/issues/22
# 使用极其简单，你只需要初始化 hook
hook = ExampleHook()
# 再将 hook 添加到 cutter 或者 classifier 中去
cutter.add_hook(hook)
# 支持多个hook，他们会按顺序执行
hook1 = ExampleHook()
cutter.add_hook(hook1)

# 开始切割
res = cutter.cut(
    video_path,
    # 默认为0.2，即将图片缩放为0.2倍
    # 主要为了提高计算效率
    # 如果你担心影响分析效果，可以将其提高
    compress_rate=0.2,
    # block 能够对每帧进行切割并分别进行比较，计算出更加敏感的ssim值
    # 默认为2，即切为4宫格；若为4，即切为16宫格，以此类推；为1即不做切割，全图比较
    # 值得注意，如果无法整除，block是会报错的
    block=2,
)

# 在切割过程中，hook的内容会同步进行
# 在切割完成后，你就可以从hook中获取结果了！
print(hook.result)
print(hook1.result)
# ExampleHook 是将每帧的size记录下来，并没有起到实际作用
# hook.py 中还提供了非常实用的 InvalidFrameDetectHook（异常帧检测）、FrameSaveHook（将每一帧保存到指定文件夹）
# 你可以借此了解 hook 的运作原理，自行为你的业务定制 hook

# 你可以通过res获取切割结果，获取稳定状态与活动状态分别对应的区间
stable, unstable = res.get_range(
    # 判定阶段是否稳定的阈值
    # 越高则越严格（判定为稳定的区间更少）
    # 默认为 0.95 （0-1）
    threshold=0.95,
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
data_home = res.pick_and_save(
    # 这里的例子是对稳定区间进行采样
    stable,
    # 每段区间的采样数，3即每个阶段等距离截取3张图片
    # 如果涉及机器学习，建议将此值提高
    3,
    # 采样结果保存的位置
    # 不指定的话则会在当前位置生成文件夹并返回它的路径
    # './cut_result',
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
r.add_dir_link(data_home)

# 你可以将 thumbnail 直接嵌入到report中
for each in unstable:
    r.add_thumbnail(
        f'{each.start}({each.start_time}) - {each.end}({each.end_time})',
        res.thumbnail(each))

# 你可以将把一些文件夹路径插入到报告中
# 这样你可以很方便地从报告中查看各项相关内容
# 当然，你需要想好这些路径与报告最后所在位置之间的相对位置，以确保他们能够被访问到
# r.add_dir_link(data_home)

# 在0.3.2及之后的版本，你可以在报告中加入一些自定义内容 （https://github.com/williamfzc/stagesepx/issues/13）
# r.add_extra('here is title', 'here is content')
r.draw(classify_result)
