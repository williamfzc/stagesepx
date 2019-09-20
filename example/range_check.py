from stagesepx.cutter import VideoCutter


video_path = '../demo.mp4'

cutter = VideoCutter()
res = cutter.cut(video_path)
stable, _ = res.get_range()

# 检查最后一个阶段中是否包含图片 person.png
res = stable[-1].contain_image('../person.png')

print(res)
# eg:
# {'target_point': [550, 915], 'target_sim': 0.9867244362831116, 'ok': True}
