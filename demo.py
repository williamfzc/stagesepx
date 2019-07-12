from stagesepx.cutter import VideoCutter

c = VideoCutter()
res = c.convert_video_into_ssim_list('demo_video.mp4')
res = c.get_stable_range(res)
for i in res:
    print(i)
