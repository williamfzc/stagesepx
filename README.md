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

## License

[MIT](LICENSE)

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fwilliamfzc%2Fstagesepx.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fwilliamfzc%2Fstagesepx?ref=badge_large)
