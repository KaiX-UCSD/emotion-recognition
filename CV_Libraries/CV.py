import cv2 as cv
from FaceDetection import FaceDetection
from EmotionRecognition import EmotionRecognition
"""
CV.py
CV is the main class to handle our main functions for computer vision. 
These functions include: finding a face, processing emotion, 
and moving the servos to find the face.

boolean findFace()
void servoTrackFace()
string processEmotion()
"""
class CV:

	def __init__(self,onComputer=True):
		self.faceDetect = FaceDetection(onComputer=onComputer)
		self.emotionDetect = EmotionRecognition()

		self.img = None

	"""
	findFace()
	When called this functions activates the camera and returns a boolean if
	a face is found.
	:return: (image, boolean) - (image from opencv, if Face found, true. Otherwise, false)
	"""
	def findFace(self):
		# enable camera
		cap = cv.VideoCapture(0)
		# adjust dimensions according to faceDetect
		cap.set(cv.cv.CV_CAP_PROP_FRAME_WIDTH, self.faceDetect.FRAME_WIDTH)
		cap.set(cv.cv.CV_CAP_PROP_FRAME_HEIGHT, self.faceDetect.FRAME_HEIGHT)
		# Capture frame-by-frame
		ret, frame = cap.read()
		cv.flip(frame, 1, frame)  # flip the image
		
		self.img = self.faceDetect.detect_face(frame);

		# Release capture
		cap.release()
		cv.destroyAllWindows()

		return (self.img, self.img is not None)

		
	"""
	servoTrackFace()
	When called, this will track a face detected in the camera indefinetly.
	:return: none
	"""
	def servoTrackFace(self):
		# enable camera
		cap = cv.VideoCapture(0)
		# adjust dimensions according to faceDetect
		cap.set(cv.cv.CV_CAP_PROP_FRAME_WIDTH, self.faceDetect.FRAME_WIDTH)
		cap.set(cv.cv.CV_CAP_PROP_FRAME_HEIGHT, self.faceDetect.FRAME_HEIGHT)
		while(1):
			# Capture frame-by-frame
			ret, frame = cap.read()
			cv.flip(frame, 1, frame)  # flip the image

			img = self.faceDetect.detect_face(frame);
			self.faceDetect.move_camera()
		# Release capture
		cap.release()
		cv.destroyAllWindows()	

	"""
    processEmotion()
    When called this function returns the emotion of person in the image.
    Must be called after a sucessful face detection.
    :return: string either ['anger', 'contempt', 'disgust', 'fear', 'happiness', 'neutral', 'sadness',
                         'surprise']
    """
	def processEmotion(self, img):
		result = self.emotionDetect.analyze_image(img)
		return (self.emotionDetect.get_top_emotion(result))

