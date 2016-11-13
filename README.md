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

Getting started on Windows:
1) Install Python 2.7
	-Save on C:\Python\

2) Install NumPy library:
	i)   Download numpy-1.11.2+mkl-cp27-cp27m-win32.whl from:
		www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
	ii)  Save the file on C:\Python\Scripts
	iii) Run cmd fron the above loction and type:
		pip install numpy-1.11.2+mkl-cp27-cp27m-win32.whl

NOTE: You can try installing a newer numpy if the 1.11.2 is too old.

3) Install OpenCV library:
	i) Follow same steps as (2) except you install the opencv library:
		opencv_python-2.4.13-cp27m-win32.whl


