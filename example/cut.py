from stagesepx.cutter import VideoCutter

# 改为你的视频路径
video_path = '../test.mp4'

cutter = VideoCutter(
    # 步长，默认为1，通过它可以自行把握效率与颗粒度
    # 设定为2时，会以2帧为一个单位进行遍历
    # 即跳过一帧
    step=1,
    # 默认为0.2，即将图片缩放为0.2倍
    # 主要为了提高计算效率
    compress_rate=0.2
)

# 开始切割
res = cutter.cut(video_path)

# 你可以通过res获取切割结果
# 例如稳定状态对应的区间
# limit能够过滤掉一些过于短的阶段（例如你不希望一些持续时间过短的阶段被认为是一个稳态），默认不过滤
stable, unstable = res.get_range(
    # 判定阶段是否稳定的阈值
    # 越高则越严格（判定为稳定的区间更少）
    # 默认为 0.95 （0-1）
    threshold=0.95
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

    # 目前的 SVM分类器 不会提供默认类别（即 不像SSIM分类器一样 会将匹配不到的图像置为-1分类）
    # 所以所有的帧都会被强行分类到某一个类别中去，即便它可能不是很像
    # 如果你希望使用 SVM 分类，你最好将不稳定的部分也加入以减少误判发生（将stable替换为下面的）
    # sorted(stable + unstable, key=lambda x: x.start),

    # 每段区间的采样数，3即每个阶段等距离截取3张图片
    3,
    # 采样结果保存的位置
    # 不指定的话则会在当前位置生成文件夹并返回它的路径
    './cut_result',
)
print(f'data saved to {data_path}')
