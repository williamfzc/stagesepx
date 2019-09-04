# 为你的业务建立稳定的视频分析服务

## 思路

### 数据采集

#### 利用 cutter 自动从视频中采集

- 录制下多个你的业务场景的操作视频
- 对这些视频进行 cut 操作，得到一系列图片集
- 校验这些图片集的分类是否符合你的预期

如何采集参见 [cut.py](./cut.py)

#### 手动采集

- 自行从视频或其他方式截取一系列图片
- 自行分类，目录结构请参考 cutter 的结果

最后的目录大致形态：

![structure](https://user-images.githubusercontent.com/13421694/64073910-e8a97c80-ccd6-11e9-9847-39c3a4d277c3.png)

### 模型训练

在校验后的训练集上 train 你的模型，并保存。

- 如何训练参见 [train.py](./train.py)
- 如何二次训练参见 [retrain.py](./retrain.py)

当业务出现较大变更时，你可能需要重新训练模型或对原有模型进行二次训练。可以查看 others 中的指引。

### 应用

用稳定模型 predict 视频。

- 如何使用模型参见 [predict.py](./predict.py)

## others

- [关于分类结果修正](https://github.com/williamfzc/stagesepx/issues/48)
