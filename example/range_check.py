from stagesepx.cutter import VideoCutter
from stagesepx.classifier import SVMClassifier


video_path = "../demo.mp4"
image_path = "../person.png"

cutter = VideoCutter()
res = cutter.cut(video_path)
stable, _ = res.get_range()

# 检查最后一个阶段中是否包含图片 person.png
# 这种做法会在阶段中间取一帧进行模板匹配
match_result = stable[-1].contain_image(image_path)
print(match_result)
# 分别输出：最可能存在的坐标、相似度、计算是否正常完成
# {'target_point': [550, 915], 'target_sim': 0.9867244362831116, 'ok': True}

data_home = res.pick_and_save(stable, 5)
cl = SVMClassifier()
cl.load(data_home)
cl.train()
classify_result = cl.classify(video_path, stable, keep_data=True)
result_dict = classify_result.to_dict()

for each_stage, each_frame_list in result_dict.items():
    # 你可以通过对这些阶段进行目标检测，以确认他们符合你的预期
    # 例如，检测每一个阶段的最后一帧是否包含 ../person.png
    match_result = each_frame_list[-1].contain_image(image_path=image_path)
    print(match_result)
    # 可以根据实际需要继续拓展
