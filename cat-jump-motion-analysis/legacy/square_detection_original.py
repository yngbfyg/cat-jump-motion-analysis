import cv2
import numpy as np

vid = cv2.VideoCapture('чиж1.MOV')

while 1:
	frame = vid.read()[1]
	frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	frameBW = cv2.inRange(frameHSV, (122, 31, 222), (180, 85, 255))
	countrs = cv2.findContours(frameBW, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
	for cnt in countrs:
		cv2.drawContours(frame, [cnt], 0, (255, 0, 0), 2)
		box = cv2.minAreaRect(cnt)
		box = cv2.boxPoints(box)
		box = np.int0(box)
		print(box)
		cv2.drawContours(frame, [box], 0, (255, 255, 0), 2)
	cv2.imshow('cam 0', frame)
	key = cv2.waitKey(40)
	if key == 27:
		break
	
		
