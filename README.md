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
| python version       | [![PyPI version](https://badge.fury.io/py/stagesepx.svg)](https://badge.fury.io/py/stagesepx)                                                                                                    |
| auto test            | ![CI Status](https://github.com/williamfzc/stagesepx/workflows/smoketest/badge.svg)                                                                                                              |
| code maintainability | [![Maintainability](https://api.codeclimate.com/v1/badges/ef27756ce9a4f7f4ba94/maintainability)](https://codeclimate.com/github/williamfzc/stagesepx/maintainability)                            |
| code coverage        | [![codecov](https://codecov.io/gh/williamfzc/stagesepx/branch/master/graph/badge.svg)](https://codecov.io/gh/williamfzc/stagesepx)                                                               |
| docker build status  | ![Docker Cloud Automated build](https://img.shields.io/docker/cloud/automated/williamfzc/stagesepx) ![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/williamfzc/stagesepx) |
| code style           | [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)                                                                                 |

---

这段视频展示了一个应用的完整启动过程：

![video_readme.gif](https://i.loli.net/2019/09/01/tXRhB6ai9jAZFmc.gif)

将视频传递给 stagesepx，它将自动分析拆解，得到视频中所有的阶段。包括变化的过程及其耗时，以及在稳定的阶段停留的时长：

![taobao_startup.png](https://i.loli.net/2019/11/23/Cio39V4AhmWOyFL.png)

你可以据此得到每个阶段对应的精确耗时。当然，它是天然跨端的，例如web端。甚至，任何端：

![sugar.gif](https://i.loli.net/2019/11/23/BCjI8PiJrgmxQUt.gif)

![sugar](https://i.loli.net/2019/11/23/DCpbdlNftcQ3v2w.png)

与视频一致的高准确度。以秒表为例：

![accuracy.png](https://i.loli.net/2019/10/02/Cboj743UwRQmgPS.png)

可以看到，与秒表的表现几乎没有差异。

---

- 全自动，无需前置训练与学习
- 更少的代码需要
- 高度可配置化，适应不同场景
- 支持与其他框架结合，融入你的业务
- 所有你需要的，只是一个视频

## 快速开始

- [用30行代码快速跑一个demo](example/mini.py)
- [30行代码怎么没有注释？](example/cut_and_classify.py)
- [老板让我看看这个项目怎么落地](example)
- [我有问题要问](https://github.com/williamfzc/stagesepx/issues/new)
- [官方文档](https://williamfzc.github.io/stagesepx/)

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
- ...

## License

[MIT](LICENSE)

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fwilliamfzc%2Fstagesepx.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fwilliamfzc%2Fstagesepx?ref=badge_large)
