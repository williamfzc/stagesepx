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

stagesepx 将 自动侦测出所有处于稳定的阶段：

![stable.png](https://i.loli.net/2019/09/01/bRtMZJvzLilpUW5.png)

并绘制出稳定阶段之间的变化过程：

![unstable2.png](https://i.loli.net/2019/09/01/T72quGI5m1SlzNF.png)

![unstable1.png](https://i.loli.net/2019/09/01/ifotzbhTaDpqQFA.png)

轻松查看每个阶段的耗时：

![Trend-2.png](https://i.loli.net/2019/09/01/Tz2tZQ5e3vHBWJ6.png)

![Time Cost.png](https://i.loli.net/2019/09/01/erK9mPsISbHEiFO.png)

原生跨平台，不只是移动端：

![web.gif](https://i.loli.net/2019/11/05/bQr18d6l9fNjIhS.gif)

![web.png](https://i.loli.net/2019/11/05/ywZ9qag3rslNKx6.png)

甚至，任何场景：

[![pen.gif](https://i.loli.net/2019/07/22/5d35a84e3e0df82450.gif)](https://i.loli.net/2019/07/22/5d35a84e3e0df82450.gif)

[![pen_chart.png](https://i.loli.net/2019/07/22/5d35a8858640e67521.png)](https://i.loli.net/2019/07/22/5d35a8858640e67521.png)

与视频一致的高准确度。以秒表为例：

![accuracy.png](https://i.loli.net/2019/10/02/Cboj743UwRQmgPS.png)

---

- 全自动，无需前置训练与学习
- 更少的代码需要
- 高度可配置化，适应不同场景
- 支持与其他框架结合，融入你的业务
- 所有你需要的，只是一个视频

## 快速开始

- 直接 [通过命令行使用](example)
- 一个 [仅有30行的例子](example)
- 完善的 [官方文档](https://williamfzc.github.io/stagesepx/)

## License

[MIT](LICENSE)

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fwilliamfzc%2Fstagesepx.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fwilliamfzc%2Fstagesepx?ref=badge_large)
