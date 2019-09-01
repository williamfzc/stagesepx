"""
这个例子描述了如何训练一个后续可用的模型

在 cut 流程之后，你应该能得到一个已经分拣好的训练集文件夹
我们将基于此文件夹进行模型的训练
"""
from stagesepx.classifier import SVMClassifier

DATA_HOME = './cut_result'
cl = SVMClassifier()

# 加载数据
cl.load(DATA_HOME)
# 在加载数据完成之后需要先训练
cl.train()
# 在训练后你可以把模型保存起来
cl.save_model('model.pkl')
