from stagesepx.cutter import VideoCutter
from stagesepx.classifier import SVMClassifier

video_path = "../demo.mp4"
amazon_image_path = "../amazon.png"
phone_image_path = "../phone.png"
message_image_path = "../message.png"

cutter = VideoCutter()
res = cutter.cut(video_path)
stable, _ = res.get_range()

# 检查最后一个阶段中是否包含图片 person.png
# 这种做法会在阶段中间取一帧进行模板匹配
# 当然，这种做法并不常用，最常用还是用于检测最终结果而不是中间量
# 值得注意，这里的模板匹配会受到压缩率的影响
# 虽然已经做了分辨率拟合，但是如果压缩率过高，依旧会出现图像难以辨认而导致的误判
# 正常来说没什么问题
match_result = stable[-1].contain_image(
    amazon_image_path, engine_template_scale=(0.5, 2, 5)
)
print(match_result)
# 分别输出：最可能存在的坐标、相似度、计算是否正常完成
# {'target_point': [550, 915], 'target_sim': 0.9867244362831116, 'ok': True}

data_home = res.pick_and_save(stable, 5)
cl = SVMClassifier()
cl.load(data_home)
cl.train()
classify_result = cl.classify(video_path, stable, keep_data=True)
result_dict = classify_result.to_dict()

final_result: dict = {}

for each_stage, each_frame_list in result_dict.items():
    # 你可以通过对这些阶段进行目标检测，以确认他们符合你的预期
    # 注意，如阶段名称为负数，意味着这个阶段是处在变化中，非稳定
    # 例如，检测每一个阶段的中间帧是否包含特定图片
    middle_id: int = int((len(each_frame_list) - 1) / 2)

    # 分别检测 amazon.png 与 phone.png （这两张是手动选出来的标志物）
    amazon_image_res = each_frame_list[middle_id].contain_image(
        image_path=amazon_image_path,
        # 模板匹配依赖了 findit
        # 所有 findit 需要的参数都可以通过 kwargs 的形式传递并生效
        # 具体可查看 FindIt object 的 __init__() 与 find()
        engine_template_scale=(0.5, 2, 10),
    )
    phone_image_res = each_frame_list[middle_id].contain_image(
        image_path=phone_image_path, engine_template_scale=(0.5, 2, 10)
    )
    msg_image_res = each_frame_list[middle_id].contain_image(
        image_path=message_image_path, engine_template_scale=(0.5, 2, 10)
    )
    final_result[each_stage] = {
        amazon_image_path: amazon_image_res["target_sim"],
        phone_image_path: phone_image_res["target_sim"],
        message_image_path: msg_image_res["target_sim"],
    }

# 可以通过这些标志物知晓阶段是否符合预期，并进行计算
print(final_result)
