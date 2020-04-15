import cv2
import numpy as np
import imutils
cap = cv2.VideoCapture(0)

ret, frame1 = cap.read()
ret, frame2 = cap.read()

while cap.isOpened():

	diff = cv2.absdiff(frame1, frame2)
	gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray, (5, 5), 0)
	_, thresh = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY)
	dilated = cv2.dilate(thresh, None, iterations=4)
	contours = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	contours = imutils.grab_contours(contours)
	for contour in contours:
			(x, y, w, h) = cv2.boundingRect(contour)
			if cv2.contourArea(contour) < 700:
					continue
			cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 0, 255), 2)
	cv2.imshow('Motion Detector', frame1)
	frame1 = frame2

	ret, frame2 = cap.read()
	if cv2.waitKey(40) == 27:
			break
cap.release()

cv2.destroyAllWindows()