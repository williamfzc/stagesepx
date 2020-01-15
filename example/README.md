# example for stagesepx

## 安装

支持 python3.6 及更高的版本。

```bash
pip install stagesepx
```

你可以通过源码安装来获取还未发布的最新版本：

```bash
git clone https://github.com/williamfzc/stagesepx.git
cd stagesepx
pip install .
```

## 快速开始

> 如果你只是想落地，可以先看看 [实际应用的例子](https://github.com/williamfzc/work_with_stagesepx)

### 命令行方式

stagesepx支持直接从命令行启动。在此模式下，你无需编写任何代码。

试着分析你的第一个视频：

```bash
stagesepx one_step demo.mp4
```

### 脚本方式

如果你想要更多定制，或者你希望与其他程序进行结合，那么你最好通过脚本使用。

- [mini.py](./mini.py) 提供了一个不到30行的例子。当然，这也意味着肯定不会包含太多功能。
- [cut_and_classify.py](./cut_and_classify.py) 提供了几乎所有的stagesepx用法及详细的注释。

你可以先从前者开始使用，再根据自身的需要，参考后者的用法逐步补充到前者中。

### docker image

基于docker，我们提供了更为简洁的方式使它能够运行在容器内。你无需关心复杂的依赖，并且能够更轻松地与其它系统（诸如Jenkins）结合。

例如你的视频放置在 `video_dir` 目录下，名为 `demo.mp4`：

```bash
cd video_dir
```

创建并启动容器：

```bash
docker run \
    --rm \
    -v ${PWD}:/usr/src/app \
    williamfzc/stagesepx \
    stagesepx one_step demo.mp4
```

当然你也可以使用脚本方式：

```bash
docker run \
    --rm \
    -v ${PWD}:/usr/src/app \
    williamfzc/stagesepx \
    python your_script.py
```

## 常规落地方案

常规情况下，有一个比较通用的落地方案：

- 视频采集器
    - 根据你的实际情况可能不同
    - 可能是硬件（摄像头）或者软件（录屏工具？）
    - 向下游提供过程录制服务
- 自动化驱动
    - 通常是UI自动化框架
    - 在录制过程中代替人进行操作
    - 与视频采集器配合，不断向下游提供录制完成的视频
- stagesepx
    - 逐一分析视频，得到结果
    
如此做后，这整套东西可以形成闭环。你可以将其与CI系统结合，制造一套稳定的工作流。

## 落地指南

经过上述流程，你会拥有一套稳定可以持续运行的工作流。而此时，你可能面临的问题是：

- 我不需要那么多的阶段 / 我希望合并阶段
- 我依然需要人工来检查这些结果
- 每次分出来的阶段数量似乎有可能不同
- ...

[这个例子](./train_and_predict) 将引导你解决上述的问题，顺利将它落地到实际业务中。

## 视频比较（实验性质）

视频比较功能被设计用于功能层面上的校验。通过视频比较，你可以先录制好一个人工校验无误的视频，然后：

- 检验不同分辨率下的表现是否一致
- 在多次重复流程中，检验他们的表现是否一致
- ...

参见 [compare_videos.py](./compare_videos.py)。

## 常见问题

### 为什么分出来的阶段不符合我的预期？

有个前提，人类的视觉感知实际上不是非常灵敏。很多情况下，人类认知的稳定状态实际上并不是真正意义上的稳定。当阈值很高时，这种情况出现的概率会逐步上升，你可能会很奇怪为什么分出来的阶段如此之多。

立竿见影的解决方案是，略微降低阈值，使其不那么敏感。对于大多数情况（例如页面切换）还是非常奏效的，因为这种情况下改变非常剧烈，计算得到的相似度要远低于阈值；而与此同时一些诸如噪音的干扰可以被阈值过滤掉。

如果你遇到的问题是，很多你觉得应该分出来的阶段没有被自动识别出来，那你可以将阈值调高。在这一层面，机器的判定能力要远强于人类。

### 如何自动化地检测每个阶段是否符合我的预期？

`VideoCutRange` 内置的 `contain_image` 方法使你能够检测某个阶段中的帧是否包含某个特定icon。例如，你的场景中结束的标志是A icon出现，你可以利用这种方法检测A icon是否出现在最后一个稳定阶段中，以此判断场景是否正常结束。

你可以通过这种方法对 cutter 的结果进行检测。参考 [range_check.py](./range_check.py)。

### 如何自动化处理最终的分类结果而不是报告？

之所以会有这个疑惑，很大程度上是因为 stagesepx 自带了 report 系统，而 [例子](./mini.py)中把处理结果直接渲染成报告展示出来了。

那么这个问题的答案也很简单，你只需要直接处理交给 reporter 的数据就可以了，他们两者并没有耦合关系。

```python
# 分类出来的结果是一个 list，里面包含 ClassifierResult 对象
# 如果你希望这个东西能够接入你的业务，与其他的工具协同，那么光靠后面的报告其实意义不大
# 你可以基于 classify_result 进行定制化开发
for each in classify_result:
    # 它的帧编号
    print(each.frame_id)
    # 它的时间戳
    print(each.timestamp)
    # 它被划分为什么类型
    print(each.stage)
    break
```

具体可以参考 [完整例子](./cut_and_classify.py)。

### 如何定制我的阶段切割结果？

在前面一个问题的基础上，很多人会有进一步的疑问：我认为分出来的阶段客观上符合逻辑，但是我希望自己决定如何分阶段。

当然是可以的。在生产环境的业务上，这种方式是首选的。我也不相信你会有勇气把没有人工干预过的全自动化工具放上正式环境。

首先你需要明白 cutter 与 classifier 是如何运作的（可参见[HOW_IT_WORKS](https://williamfzc.github.io/stagesepx/#/pages/3_how_it_works) 一节）。实际上阶段的划分是由 cutter 来决定的。换言之，我们只需要对 cutter 的行为进行干预，即可进一步控制阶段分割结果。

更简单的方法是，直接人工处理 cutter 的结果，用人工分拣过的数据集训练模型。这样做，你的模型会完全根据你挑选出来的数据集生成。
