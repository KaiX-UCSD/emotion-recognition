# Emotion Recognition
Software for detecting identity of faces and classifying their emotion.

To run on your Mac/Linux:
	To run the facial tracking on your PC's webcam run the command:
		python face-recognition-video.py

To run on the raspberry pi:

The raspberry pi code is contained in Facetrack.py. This code utilizes
the face video algorithm and the CamControl library to control a webcam
to follow a face. To run go into the emotion-regcognition directory and call:

$ python Facetrack.py

Raspberry Pi Setup:

Libraries to install on the raspberry pi:
Update and upgrade existing packages
	
	$ sudo apt-get update
	$ sudo apt-get upgrade

Install python 2.7 dev tools:

	$ sudo apt-get install python2.7

If numpy is not already installed, then 

	$ sudo apt-get install python-numpy

To install opencv2
	
	$ sudo apt-get install python-opencv
	$ sudo apt-get install python-scipy
	$ sudo apt-get install ipython
	
Install ServoBlaster onto pi as said in the readme of 
	https://github.com/richardghirst/PiBits/tree/master/ServoBlaster
	(the user space daemon). Here is a barebones excerpt of the instructions
ServoBlaster - The user space daemon
-----------------------------------
Clone this repository into your folder: https://github.com/richardghirst/PiBits/tree/master/ServoBlaster/user
To use this daemon grab the servod.c source and Makefile and:

$ make servod

To have the servod start automatically when the system boots, then you can
install it along with a startup script as follows:

$ sudo make install 

If you don't want is to start automatically, then run this command on:

$ sudo ./servod

The prompt will return immediately, and servod is left running in the background.  
You can check it is running via the "ps ax" command. If you want to stop servod,
the easiest way is to run:

$ sudo killall servod

Note that the use of PWM will interfere with the 3.5mm jack audio output.


Getting started on Windows:
---------------------------
1) Install Python 2.7
	-Save on C:\Python\

2) Install NumPy library:
	i)   Download numpy-1.11.2+mkl-cp27-cp27m-win32.whl from:
		www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
	ii)  Save the file on C:\Python\Scripts
	iii) Run cmd fron the above loction and type:
 $ pip install numpy-1.11.2+mkl-cp27-cp27m-win32.whl

NOTE: You can try installing a newer numpy if the 1.11.2 is too old.

3) Install OpenCV library:
	i) Follow same steps as (2) except you install the opencv library:
		opencv_python-2.4.13-cp27m-win32.whl

