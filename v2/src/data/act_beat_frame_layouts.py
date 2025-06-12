ACT_BEAT_FRAME_LAYOUTS = {}

for i in range(200):
    if i < 9:
        ACT_BEAT_FRAME_LAYOUTS[i] = (i, 1)
    else:
        frame = 8
        beat = (i - 9) // 8 + 2
        ACT_BEAT_FRAME_LAYOUTS[i] = (frame, beat)
