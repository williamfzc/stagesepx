from stagesepx.cutter import VideoCutter

c = VideoCutter(period=10)
res = c.cut('video/demo_video.mp4')
stable = res.get_stable_range()
unstable = res.get_unstable_range()

for each_unstable in unstable:
    print(each_unstable)
    print(each_unstable.pick(2)[0])
