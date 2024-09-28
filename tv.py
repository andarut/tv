import os
import time

os.system("clear")

def resize_terminal(width: int, height: int):
	os.system(f"resize -s {height} {width}")

import cv2 as cv

def get_video_metadata(path: str):
	cap = cv.VideoCapture(path)
	if cap.isOpened():
		width  = cap.get(cv.CAP_PROP_FRAME_WIDTH)
		height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
		fps = cap.get(cv.CAP_PROP_FPS)
		frame_count = cap.get(cv.CAP_PROP_FRAME_COUNT)
	cap.release()
	duration = frame_count / fps
	return int(width), int(height), int(fps), int(frame_count), int(duration)

import numpy as np
from PIL import Image

def play_video(path):

	frames = []
	pixel_ascii_map = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
	cap = cv.VideoCapture(path)

	j = 1
	while cap.isOpened():
		ret, frame = cap.read()
		if not ret:
			break

		frame_image = Image.fromarray(cv.cvtColor(frame, cv.COLOR_BGR2RGB))
		frame_width, frame_height, fps, frame_count, duration = get_video_metadata(path)
		print(f"[FRAME][{j} / {frame_count}] = {(frame_width, frame_height, fps, frame_count, duration)}")
		resize_terminal(frame_width, frame_height)
		frame_buf = ""

		data = list(frame_image.getdata())

		i = 1
		for pixel in iter(data):
			value = (sum(pixel) // 3) * len(pixel_ascii_map) // 255
			# if value == len(pixel_ascii_map):
			# 	value -= 1
			# try:
			ascii_val = pixel_ascii_map[value-1]
			# except IndexError:
			# 	print(value, len(pixel_ascii_map))
			frame_buf += ascii_val
			if i % frame_width == 0:
				frame_buf += "\n"
			i += 1
		frames.append(frame_buf)
		j += 1

	cap.release()
	cv.destroyAllWindows()

	start = time.time()
	for frame in frames:
		print(frame, end="\r")
		time.sleep(0.1 / 4 * 1.1)

	end = time.time()
	print(end - start)

play_video("demo.mp4")
