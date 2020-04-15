import cv2
from skimage import exposure, feature

cap = cv2.VideoCapture(0) 

while cap.isOpened():
	ret, image = cap.read()
	if not ret:
		break

	(H, hogImage) = feature.hog(image, orientations=3, pixels_per_cell=(16, 16),
		cells_per_block=(2, 2), transform_sqrt=True, block_norm="L1",
		visualize=True)
	hogImage = exposure.rescale_intensity(hogImage, out_range=(0, 255))
	hogImage = hogImage.astype("uint8")
	
	cv2.imshow("HOG VIZ", hogImage)

	if cv2.waitKey(40) == 27:
		break

cap.release()