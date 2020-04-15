import cv2
from time import time
from PIL import Image, ImageDraw, ImageFont
import numpy as np

buffer_size = 3
cap = cv2.VideoCapture(0)
font = ImageFont.truetype('./Blazed.ttf', size=24)
fps = 0.0

prev = cv2.GaussianBlur(cap.read()[1], (7,7), 0.0) # DON'T!

while cap.isOpened():
	start = time()
	ret, image = cap.read()
	if not ret: # It means that capture failed
		print('That\'s unfortunate.')
		break

	# We blur the image to reduce the noise
	blur = cv2.GaussianBlur(image, (7,7), 0.0)

	# It explains itself
	delta = cv2.absdiff(prev, blur)

	# It looks cool, I love it, I show it!  
	cv2.imshow('Delta', delta)

	# A new array is created, but this one hold 32 bit values instead of 8
	delta_sum = np.zeros(blur.shape[:2], np.uint32)#overflow

	# We add up the difference of each color channel
	# Because why not overcomplicate things
	# The first one is blue, secon=d green and third is red
	delta_sum = delta[:,:,0].astype(np.uint32) + delta[:,:,1].astype(np.uint32) + delta[:,:,2].astype(np.uint32)
	
	# This makes everything over 255 into 255 to turn it into 255
	# I'll explain it why
	delta_sum = np.where(delta_sum > 255, np.ones_like(delta_sum)*255, delta_sum).astype(np.uint8)

	# The input is thresholded to make it less ghosty and more well defined
	_, delta_sum = cv2.threshold(delta_sum, 127, 255, cv2.THRESH_BINARY)

	# About this we care about how it looks like
	cv2.imshow('Sum', delta_sum)


	# DRAWING STUFF
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
	image = Image.fromarray(image)
	draw = ImageDraw.Draw(image)
	
	draw.text(text=f'{fps:.2f} FPS', xy=(10, 10), fill=(255,255,255), font=font)

	image = np.array(image)

	image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
	cv2.imshow('Clean', image)

	if cv2.waitKey(40) == 27:
		break
	
	prev = blur
	end = time()
	fps = 1.0/(end-start)

cap.release()