from time import time

import cv2
import numpy as np
from imutils import grab_contours, resize
from imutils.object_detection import non_max_suppression
from PIL import Image, ImageDraw, ImageFont

# The capture object
# 0 usually means the default camera
# If you have an external webcam, then try 1 or 2
cap = cv2.VideoCapture(0) 

# DA FONT
font = ImageFont.truetype('./Blazed.ttf', size=24)

# Initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# This is here only for the first iteration
fps = 0.0
prev = resize(cap.read()[1], width=400) # DON'T!
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

	image = resize(image, width=400)

	# We blur the image to reduce the noise
	blur = image.copy()

	# It explains itself
	delta = cv2.absdiff(prev, blur)

	# It looks cool, I love it, I show it!  
	cv2.imshow('Delta', delta)

	# A new array is created, but this one hold 32 bit values instead of 8
	delta_sum = np.zeros(blur.shape[:2], np.uint32)#overflow

	# We add up the difference of each color channel
	# Because why not overcomplicate things
	# The first one is blue, secon=d green and third is red
	delta_sum = delta[:,:,0].astype(np.uint32) + delta[:,:,1].astype(np.uint32)\
		+ delta[:,:,2].astype(np.uint32)
	
	# This makes everything over 255 into 255 to turn it into 255
	# I'll explain why
	delta_sum = np.where(delta_sum > 255, np.ones_like(delta_sum)*255, delta_sum).astype(np.uint8)

	# The input is thresholded to make it less ghosty and more well defined
	_, delta_sum = cv2.threshold(delta_sum, 80, 255, cv2.THRESH_BINARY)

	# About this we care about how it looks like
	cv2.imshow('Sum of deltas', delta_sum)

# THE CODE FOR SEESION 3 STARTS HERE

	# Detect people in the image
	# This is what makes it slow
	rects, weights = hog.detectMultiScale(image, winStride=(4, 4),
		padding=(8, 8), scale=1.05)

	# Apply non-maxima suppression to the bounding boxes using a
	# fairly large overlap threshold to try to maintain overlapping
	# boxes that are still people
	rects = np.array([[x, y, x + w, y + h] for (x, y, w, h), conf in zip(rects, weights) if conf > 0.66])
	pick = non_max_suppression(rects, probs=None, overlapThresh=0.55)

	# Let's see who moved!
	colors = []
	for (xA, yA, xB, yB) in pick:
		total_size = delta_sum[xA:xB, yA:yB].size
		if total_size == 0:
			colors.append((0, 0, 255))
		elif np.count_nonzero(delta_sum[xA:xB, yA:yB])/total_size > 0.005:
			colors.append((255, 0, 0))
		else:
			colors.append((0, 255, 0))

# AND ENDS HERE

	# DRAWING STUFF

	# Pillow works with RGB images an OpenCV reads them as BGR
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)

	# Drawy thingy
	image = Image.fromarray(image)
	draw = ImageDraw.Draw(image)
	draw.text(text=f'{fps:.2f} FPS', xy=(10, 10), fill=(255,255,255), font=font)

	# Draw the final bounding boxes
	for (xA, yA, xB, yB), color in zip(pick, colors):
		draw.rectangle((xA, yA, xB, yB), outline=color)
		# cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

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
