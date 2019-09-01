# 使用

## 安装

Python >= 3.6

```python
pip install stagesepx
```

## 快速开始

?> sample code中提供了详细的注释。

[完整例子](https://github.com/williamfzc/stagesepx/tree/master/example#all-in-one) 包括了三个部分：拆分阶段、分析视频、生成报告。你可以用它快速开始试用 stagesepx。

例子中使用的视频可以[点此](https://raw.githubusercontent.com/williamfzc/stagesep2-sample/master/videos/demo.mp4)下载。

## 为你的业务建立稳定的视频分析服务

参见 [这里](https://github.com/williamfzc/stagesepx/tree/master/example#训练与预测)

## 视频比较（实验性质）

参见 [这里](https://github.com/williamfzc/stagesepx/tree/master/example#视频比较实验性质)

...

### 优异的性能表现

在效率方面，吸取了 [stagesep2](https://github.com/williamfzc/stagesep2) 的教训（他真的很慢，而这一点让他很难被用于生产环境），在项目规划期我们就将性能的优先级提高。对于该视频而言，可以从日志中看到，它的耗时在惊人的300毫秒左右（windows7 i7-6700 3.4GHz 16G）：

```bash
2019-07-17 10:52:03.429 | INFO     | stagesepx.cutter:cut:200 - start cutting: test.mp4
...
2019-07-17 10:52:03.792 | INFO     | stagesepx.cutter:cut:203 - cut finished: test.mp4
```

除了常规的基于图像本身的优化手段，stagesepx主要利用采样机制进行性能优化，它指把时间域或空间域的连续量转化成离散量的过程。由于分类器的精确度要求较高，该机制更多被用于切割器部分，用于加速切割过程。它在计算量方面优化幅度是非常可观的，以5帧的步长为例，它相比优化前节省了80%的计算量。

当然，采样相比连续计算会存在一定的误差，如果你的视频变化较为激烈或者你希望有较高的准确度，你也可以关闭采样功能。

### 更强的稳定性

stagesep2存在的另一个问题是，对视频本身的要求较高，抗干扰能力不强。这主要是它本身使用的模块（template matching、OCR等）导致的，旋转、分辨率、光照都会对识别效果造成影响；由于它强依赖预先准备好的模板图片，如果模板图片的录制环境与视频有所差异，很容易导致误判的发生。

而SSIM本身的抗干扰能力相对较强。如果使用默认的SSIM分类器，所有的数据（训练集与测试集）都来源于同一个视频，保证了环境的一致性，规避了不同环境（例如旋转、光照、分辨率等）带来的影响，大幅度降低了误判的发生。
