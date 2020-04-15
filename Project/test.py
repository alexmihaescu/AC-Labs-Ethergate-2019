import cv2
from time import time
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# The capture object
# 0 usually means the default camera
# If you have an external webcam, then try 1 or 2
cap = cv2.VideoCapture(0) 

# DA FONT
font = ImageFont.truetype('./Blazed.ttf', size=24)

# This is here only for the first iteration
fps = 0.0
prev = cv2.GaussianBlur(cap.read()[1], (7,7), 0.0) # DON'T!
# Please don't do stuff without checking it.
# I'm a professional, I'm entitled to do stupid stuff for science!
# Do what popa says not what popa does. Please.

while cap.isOpened():
	start = time()
	ret, image = cap.read()
	if not ret: # It means that capture failed
		# See? Checking is good
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
	cv2.imshow('Sum of deltas', delta_sum)


	# DRAWING STUFF

	# Pillow works with RGB images an OpenCV reads them as BGR
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)

	# Drawy thingy
	image = Image.fromarray(image)
	draw = ImageDraw.Draw(image)
	draw.text(text=f'{fps:.2f} FPS', xy=(10, 10), fill=(255,255,255), font=font)

	# Converting it back to a format OpenCV understands
	image = np.array(image)

	# Almost cool overlay
	overlay_color = (255, 102, 255)
	alpha=0.7
	overlay = np.zeros_like(image)
	for i in range(3):
		overlay[:,:,i] = np.where(delta_sum == 255, overlay_color[i], 0)
		# It turns out pink?
	image = cv2.addWeighted(overlay, 1, image, 1, 0)

	# Converting it back to BGR, for OpenCV again
	image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
	cv2.imshow('Clean', image)

	# This is necessary, you want this to be here!
	if cv2.waitKey(40) == 27:
		break
	
	# THE AFTERPARTY
	prev = blur
	end = time()
	fps = 1.0/(end-start)

# It's nice to free stuff
cap.release() 