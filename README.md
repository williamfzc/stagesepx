<h1 align="center">
  <img src="./docs/pics/brand.svg">
</h1>

<h3 align="center">stage sep(aration) x</h3>
<p align="center">
    <em>detect stages in video automatically</em>
</p>

---

| Type                 | Status                                                                                                                                                                                            |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| package version      | [![PyPI version](https://badge.fury.io/py/stagesepx.svg)](https://badge.fury.io/py/stagesepx)                                                                                                    |
| python version       | ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/stagesepx)                                                                                                                       |
| auto test            | ![CI Status](https://github.com/williamfzc/stagesepx/workflows/smoketest/badge.svg)                                                                                                              |
| code maintainability | [![Maintainability](https://api.codeclimate.com/v1/badges/ef27756ce9a4f7f4ba94/maintainability)](https://codeclimate.com/github/williamfzc/stagesepx/maintainability)                            |
| code coverage        | [![codecov](https://codecov.io/gh/williamfzc/stagesepx/branch/master/graph/badge.svg)](https://codecov.io/gh/williamfzc/stagesepx)                                                               |
| docker build status  | ![Docker Cloud Automated build](https://img.shields.io/docker/cloud/automated/williamfzc/stagesepx) ![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/williamfzc/stagesepx) |
| code style           | [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)                                                                                 |

---

> [English README here](./README_en.md)

这段视频展示了一个应用的完整启动过程：

![video_readme.gif](https://i.loli.net/2019/09/01/tXRhB6ai9jAZFmc.gif)

将视频传递给 stagesepx，它将自动分析拆解，得到视频中所有的阶段。包括变化的过程及其耗时，以及在稳定的阶段停留的时长：

![taobao_startup.png](https://i.loli.net/2019/11/23/Cio39V4AhmWOyFL.png)

你可以据此得到每个阶段对应的精确耗时。

## 跨端运作

当然，它是天然跨端的，例如web端。甚至，任何端：

![sugar.gif](https://i.loli.net/2019/11/23/BCjI8PiJrgmxQUt.gif)

![sugar](https://i.loli.net/2019/11/23/DCpbdlNftcQ3v2w.png)

## 高准确度

与视频一致的高准确度。以秒表为例：

![accuracy.png](https://i.loli.net/2019/10/02/Cboj743UwRQmgPS.png)

可以看到，与秒表的表现几乎没有差异。**请注意，这里的准确度指的是 stagesepx 能够精确还原视频本身的数据与表现。而对于现象（例如某某时间点出现什么状态）而言，准确度很大程度上取决于视频本身，如fps/分辨率等。关于结果不准确的问题请参考 [#46](https://github.com/williamfzc/stagesepx/issues/46) 。**

## 完整自动化支持

stagesepx 最强大的特性是允许用户利用自己的训练集进行模型训练，实现全自动地进行特定阶段耗时计算。此方案能够被广泛应用到各类业务迭代中，有效降低人力消耗。具体可参见 [将 stagesepx 应用到实际业务中](https://github.com/williamfzc/work_with_stagesepx)。

---

- 标准模式下无需前置训练与学习
- 更少的代码需要
- 高度可配置化，适应不同场景
- 支持与其他框架结合，融入你的业务
- 所有你需要的，只是一个视频

## 架构

![structure](./docs/pics/stagesepx.svg)

## 快速开始

- [用30行代码快速跑一个demo](example/mini.py)
- [30行代码怎么没有注释？](example/cut_and_classify.py)
- [我想看看实际落地方案，最好有把饭喂嘴里的例子](https://github.com/williamfzc/work_with_stagesepx)
- [我们的app很复杂，能搞定吗](https://testerhome.com/topics/22215)
- [太麻烦了，有没有开箱即用、简单配置下可以落地的工具](https://github.com/williamfzc/sepmachine)
- [我有问题要问](https://github.com/williamfzc/stagesepx/issues/new)
- [官方文档](https://williamfzc.github.io/stagesepx/)

## 安装

标准版（pypi）

```bash
pip install stagesepx
```

预览版（github）：

```bash
pip install --upgrade git+https://github.com/williamfzc/stagesepx.git
```

## 常见问题

最终我还是决定通过 issue 面板维护所有的 Q&A ，毕竟问题的提出与回复是一个强交互过程。如果在查看下列链接之后你的问题依旧没有得到解答：

- 请 [新建issue](https://github.com/williamfzc/stagesepx/issues/new)
- 或在相关的 issue 下进行追问与补充
- 你的提问将不止帮助到你一个人 :)

问题列表：

- [安装过程遇到问题？](https://github.com/williamfzc/stagesepx/issues/80)
- [如何根据图表分析得出app启动的时间？](https://github.com/williamfzc/stagesepx/issues/73)
- [日志太多了，如何关闭或者导出成文件？](https://github.com/williamfzc/stagesepx/issues/58)
- [我的视频有 轮播图 或 干扰分类 的区域](https://github.com/williamfzc/stagesepx/issues/55)
- [分类结果如何定制？](https://github.com/williamfzc/stagesepx/issues/48)
- [算出来的结果不准确 / 跟传统方式有差距](https://github.com/williamfzc/stagesepx/issues/46)
- [出现 OutOfMemoryError](https://github.com/williamfzc/stagesepx/issues/86)
- [工具没法满足我的业务需要](https://github.com/williamfzc/stagesepx/issues/93)
- [为什么报告中的时间戳跟实际不一样？](https://github.com/williamfzc/stagesepx/issues/75)
- [自定义模型的分类结果不准确，跟我提供的训练集对不上](https://github.com/williamfzc/stagesepx/issues/100)
- ...

不仅是问题，如果有任何建议与交流想法，同样可以通过 issue 面板找到我。我们每天都会查看 issue 面板，无需担心跟进不足。

## 相关文章

- [图像分类、AI 与全自动性能测试](https://testerhome.com/topics/19978)
- [全自动化的抖音启动速度测试](https://testerhome.com/topics/22215)
- [(MTSC2019) 基于图像分类的下一代速度类测试解决方案](https://testerhome.com/topics/21874)

## 参与项目

### 规划

项目发展至今，基础需求已经逐步进入稳定与可用阶段。接下来的工作主要分为下面几个部分：

- 更好的业务落地方案
    - 目前 stagesepx 的落地方案更多是根据不同业务的需要进行各自的封装，而并没有提供一种非常标准的封装方案；
    - 一直没有提供的原因是，我们收集到的场景可能还太少，称之为"标准"有些牵强；
    - 如果你有好的想法、建议或者落地形式，欢迎任意形式告知我们；
- 文档补充
    - 由于时间有限，该项目的使用文档主要依靠一些 例程+注释 来说明；
    - 因为文档的缺失，很多接口与方法很难被真正利用；
    - 如果你对 stagesepx 的运作感兴趣，你可以在阅读源码的同时为它补充解释，利己利人；
- 新需求的收集与开发
    - 该项目的前期需求基本来自我个人脑洞，后期需求来自于实际业务需要；
    - 但单一的业务来源肯定是不够的，我们欢迎不同公司、行业的各种需求（具体做不做再评估:)）；
    - 或者，你希望亲自开发需求，欢迎PR；

感兴趣的同学可以通过下列方式与我联系：

- 邮箱：`fengzc@vip.qq.com`
- QQ：`178894043`

### 贡献代码

欢迎感兴趣的同学为这个项目添砖加瓦，三个必备步骤：

- （小修改可忽略）请在开始编码前留个 issue 告知你想完成的功能，因为可能这个功能已经在开发中或者已有；
- commit规范我们严格遵守 [约定式提交](https://www.conventionalcommits.org/zh-hans/)；
- 该repo有较为完善的单测与CI以保障整个项目的质量，在过去的迭代中发挥了巨大的作用。所以请为你新增的代码同步新增单元测试（具体写法请参考 tests 中的已有用例）。

## License

[MIT](LICENSE)

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fwilliamfzc%2Fstagesepx.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fwilliamfzc%2Fstagesepx?ref=badge_large)
