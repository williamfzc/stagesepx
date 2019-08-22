<h1 align="center">
  <img src="./docs/pics/brand.svg">
</h1>

<h3 align="center">stage sep(aration) x</h3>
<p align="center">
    <em>detect stages in video automatically</em>
</p>

---

[![PyPI version](https://badge.fury.io/py/stagesepx.svg)](https://badge.fury.io/py/stagesepx)
![actions](https://action-badges.now.sh/williamfzc/stagesepx)
[![Maintainability](https://api.codeclimate.com/v1/badges/ef27756ce9a4f7f4ba94/maintainability)](https://codeclimate.com/github/williamfzc/stagesepx/maintainability)

---

## stagesepx 能做什么

在软件工程领域，视频是一种较为通用的UI（现象）描述方法。它能够记录下用户到底做了哪些操作，以及界面发生了什么事情。例如，下面的例子描述了从桌面打开chrome进入amazon主页的过程：

[![openAmazonFromChrome.gif](https://i.loli.net/2019/07/17/5d2e8ed1e9d0b49825.gif)](https://i.loli.net/2019/07/17/5d2e8ed1e9d0b49825.gif)

stagesepx能够**自动侦测**并提取视频中的稳定或不稳定的阶段（例子中，stagesepx认为视频中包含三个稳定的阶段，分别是点击前、点击时与页面加载完成后）：

[![stage-min.png](https://i.loli.net/2019/07/17/5d2e97c5e3a0e96365.png)](https://i.loli.net/2019/07/17/5d2e97c5e3a0e96365.png)

然后，自动得到每个阶段对应的时间区间：

[![stage_trend.png](https://i.loli.net/2019/07/17/5d2ea6720c58d44996.png)](https://i.loli.net/2019/07/17/5d2ea6720c58d44996.png)

例如，从图中可以看出：

- 视频开始直到 0.76s 时维持在阶段0
- 在 0.76s 时从阶段0切换到阶段1
- 在 0.92s 时从阶段1切换到阶段0，随后进入变化状态（当stagesepx无法将帧分为某特定类别、或帧不在待分析范围内时，会被标记为 -1，一般会在页面发生变化的过程中出现）
- 在 1.16s 时到达阶段2
- ...

以此类推，我们能够对视频的每个阶段进行非常细致的评估。通过观察视频也可以发现，识别效果与实际完全一致。

在运行过程中，stagesepx强大的快照功能能够让你很轻松地知道每个阶段到底发生了什么：

[![thumbnail.png](https://i.loli.net/2019/07/25/5d3955365dff977571.png)](https://i.loli.net/2019/07/25/5d3955365dff977571.png)

**而所有的一切只需要一个视频，无需前置模板、无需提前学习。**

## 使用及原理

请移步 [官方文档](https://williamfzc.github.io/stagesepx/) 

## License

[MIT](LICENSE)
