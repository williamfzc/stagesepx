from stagesepx.cutter import VideoCutter

# 改为你的视频路径
video_path = '../demo.mp4'

cutter = VideoCutter(
    # 步长，默认为1，通过它可以自行把握效率与颗粒度
    # 设定为2时，会以2帧为一个单位进行遍历
    # 即跳过一帧
    step=1,
)

# 开始切割
res = cutter.cut(
    video_path,
    # 默认为0.2，即将图片缩放为0.2倍
    # 主要为了提高计算效率
    compress_rate=0.2
)

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
res.thumbnail(unstable[0], to_dir='.')

# 由于所有的阶段都是自动侦测的，可能发生的一个状况是：
# 你对同一个场景重复录制了几次视频，但可能由于拍摄效果与环境的影响，每个视频得到的阶段数量不一致
# 基于findit，用户能够直接对阶段进行检测，以确保阶段对应的内容符合预期
# 例如，你希望第二个稳定阶段中的帧必须包含某图像（路径为a.png），可以：
# assert stable[1].contain_image('a.png')

# 对区间进行采样
data_path = res.pick_and_save(
    # 这里的例子是对稳定区间进行采样
    stable,
    # 每段区间的采样数，3即每个阶段等距离截取3张图片
    # 如果涉及机器学习，建议将此值提高
    3,
    # 采样结果保存的位置
    # 不指定的话则会在当前位置生成文件夹并返回它的路径
    './cut_result',
)
print(f'data saved to {data_path}')
