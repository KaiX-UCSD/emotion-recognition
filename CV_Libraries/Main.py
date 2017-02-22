import cv2 as cv
import time
from EmotionRecognition import EmotionRecognition
from FaceDetection import FaceDetection
from CV import CV

compV = CV(True) # true for is on computer. False for on raspbery pi

image, found = compV.findFace()
if found:
	print compV.processEmotion(image)
