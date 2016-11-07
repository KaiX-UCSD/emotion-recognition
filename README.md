# Emotion Recognition
Software for detecting identity of faces and classifying their emotion.

Servo Setup:
Setup:
	Install ServoBlaster onto pi as said in the readme of 
	https://github.com/richardghirst/PiBits/tree/master/ServoBlaster
	(the user space daemon)

To run on your PC:
	To run the facial tracking on your PC's webcam run the command:
		python face-recognition-video.py

The raspberry pi code is contained in Facetrack.py. This code utilizes
the face video algorithm and the CamControl library to control a webcam
to follow a face.
