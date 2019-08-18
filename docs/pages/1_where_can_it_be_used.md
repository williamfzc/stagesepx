# 应用场景

!> stagesepx 本质上是一个视频分析工具，它本身只跟视频有关联，并没有任何特定的使用场景！你可以尽情发挥你的想象力，用它帮助你实现更多的功能。

## APP

- 前面提到的应用启动速度计算
- 那么同理，页面切换速度等方面都可以应用
- 除了性能，你可以使用切割器对视频切割后，用诸如[findit](https://github.com/williamfzc/findit)等图像识别方案对功能性进行校验
- 除了应用，游戏这种无法用传统测试方法的场景更是它的主场
- ...

## 除了APP？

- 以视频为分析主体，对运行时无依赖
- 除了移动端，当然PC、网页也可以同理计算出结果
- 甚至任何视频？

[![pen.gif](https://i.loli.net/2019/07/22/5d35a84e3e0df82450.gif)](https://i.loli.net/2019/07/22/5d35a84e3e0df82450.gif)

你可以直接得到出笔进入与移除的耗时！

[![pen_chart.png](https://i.loli.net/2019/07/22/5d35a8858640e67521.png)](https://i.loli.net/2019/07/22/5d35a8858640e67521.png)

它没有任何限制！

## As AI frontend

Stagesepx also was designed as a tool for preparation of AI processing. It can easily collect resources from videos for further image processing. Here is an example flow:

![ai_flow.png](https://i.loli.net/2019/08/15/yMbnQNx5E2Jg6S3.png)

It offered a 'bridge' between videos and image processing directly. And you do not need to handle videos by yourself.

View https://github.com/williamfzc/stagesepx/issues/28 for details.
