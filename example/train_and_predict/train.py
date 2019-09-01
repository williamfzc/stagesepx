"""
这个例子描述了如何训练一个后续可用的模型

在 cut 流程之后，你应该能得到一个已经分拣好的训练集文件夹
我们将基于此文件夹进行模型的训练
"""
from stagesepx.classifier import SVMClassifier

DATA_HOME = './cut_result'
cl = SVMClassifier(
    # 默认情况下使用 HoG 进行特征提取
    # 你可以将其关闭从而直接对原始图片进行训练与测试：feature_type='raw'
    feature_type='hog',
    # 默认为0.2，即将图片缩放为0.2倍
    # 主要为了提高计算效率
    # 如果你担心影响分析效果，可以将其提高
    compress_rate=0.2,
)

# 加载数据
cl.load(DATA_HOME)
# 在加载数据完成之后需要先训练
cl.train()
# 在训练后你可以把模型保存起来
cl.save_model('model.pkl')
