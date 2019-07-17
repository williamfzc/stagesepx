from stagesepx.classifier import SVMClassifier
from stagesepx.reporter import Reporter


# 默认情况下使用 HoG 进行特征提取
# 你可以将其关闭从而直接对原始图片进行训练与测试：feature_type='none'
cl = SVMClassifier(feature_type='hog')

# 基本与SSIM分类器的流程一致
# 但它对数据的要求可能有所差别，具体参见 cut.py 中的描述
cl.load('./cut_result')

# 在加载数据完成之后需要先训练
cl.train()

# # 在训练后你可以把模型保存起来
# cl.save_model('model.pkl')
# # 或者直接读取已经训练好的模型
# cl.load_model('model.pkl')

# 开始分类
res = cl.classify('../test.mp4')

Reporter.draw(
    res,
    report_path='report.html'
)
