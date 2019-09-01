# 为你的业务建立稳定的视频分析服务

## 思路

- 录制下多个你的业务场景的操作视频
- 对这些视频进行 cut 操作，得到一系列图片集
- 手动校验这些图片集的分类是否符合你的预期
- 在校验后的训练集上 train 你的模型，并保存
- 用稳定模型 predict 视频

## example

- cut 操作参见 `cut.py`
- train 操作参见 `train.py`
- predict 操作参见 `predict.py`

## others

- [关于分类结果修正](https://github.com/williamfzc/stagesepx/issues/48)
