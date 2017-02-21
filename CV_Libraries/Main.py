import cv2 as cv
import time
from EmotionRecognition import EmotionRecognition
from FaceDetection import FaceDetection


faceDetect =  FaceDetection()
emotRecog = EmotionRecognition()

FRAME_WIDTH = 320
FRAME_HEIGHT = 240
cap = cv.VideoCapture(0)
cap.set(cv.cv.CV_CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv.cv.CV_CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

time.sleep(1)
while True:
	# Capture frame-by-frame
	ret, frame = cap.read()
	cv.flip(frame, 1, frame)  # flip the image

	# faceDetect.debugging_script(cascPath='../cascades/haarcascade_frontalface_default.xml')
	img = faceDetect.face_detect(frame)

	# TODO run on separate thred
	if( img is not None):
		print("anaylizing images")
		result = emotRecog.analyze_image(img)
		print(emotRecog.get_top_emotion(result))

	# faceDetect.move_camera(cFace) only used on raspberry pi
	cv.imshow("View", frame)
	if cv.waitKey(1) & 0xFF == ord('q'):
		break

# Release capture
cap.release()
cv.destroyAllWindows()