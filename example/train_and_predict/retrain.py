"""
二次训练

在业务变更时，难免出现需要调整模型的情况
- 如果业务变更较大，推荐重新训练新模型
- 如果业务变更不大，可以按照下面的方法对原有模型进行调整
"""

from stagesepx.classifier import SVMClassifier

DATA_HOME = './cut_result'
cl = SVMClassifier()

# 加载数据
cl.load(DATA_HOME)
# 加载旧模型
cl.load_model('model.pkl')
# 在加载数据完成之后需要先训练
cl.train()
# 保存新模型
cl.save_model('new_model.pkl')

# 或者你可以直接覆盖掉旧的模型
# cl.save_model('model.pkl', overwrite=True)
