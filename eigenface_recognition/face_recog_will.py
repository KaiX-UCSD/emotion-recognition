import numpy as np
import cv2, glob, os, time
from picamera import PiCamera
from picamera.array import PiRGBArray

face_size = (60,60)

def load_recognizer(file):
    recognizer = cv2.createEigenFaceRecognizer()
    t1 = time.time()
    recognizer.load(file)
    t2 = time.time()
    print 'Time for loading recognizer:', t2-t1
    print 'loading complete'
    return recognizer

if __name__ == '__main__':
    
    # initialize face recognizer
    cascade_path = 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)
    recognizer = load_recognizer('willface.xml')

    # initialize camera
    camera = PiCamera()
    width = 640
    height = 480
    camera.rotation = 180
    camera.resolution = (width,height)#TODO
    #camera.framerate = 2
    rawCapture = PiRGBArray(camera, size=(width,height))

    # warm up and set up
    print 'Warming Up ... 3 seconds'
    time.sleep(3)
    avg = None
    motionCounter = 0
    th = 10 #TODO thresh value for difference image
    min_area = 1000 #TODO min area to filter small contours in diff image
    text = ''
    font = cv2.FONT_HERSHEY_SIMPLEX
    print 'Starting ...'

    for f in camera.capture_continuous(rawCapture, format='bgr',use_video_port=True):
        frame = f.array
        frame = cv2.resize(frame, (width/2, height/2))
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #time.sleep(0.5)
        label_real = 2
        t1 = time.time()
        faces = face_cascade.detectMultiScale(img)    
        for (x,y,w,h) in faces:
            face = img[y:y+h, x:x+w]
            face = cv2.resize(img,face_size)
            label_pred, conf = recognizer.predict(face)
            if label_pred == label_real and conf<900:
                text = 'Will'
                print '{} is correctly recognized with confidence {}.'.format(label_real, conf)
            else:
                text = '?'
        t2 = time.time()
        print 'Time for face recognition:', t2-t1
        #print len(faces)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            cv2.putText(frame, text, (x,y), font, 1, (0,255,0), 2)
        cv2.imshow('Output', frame)
        cv2.waitKey(50)
        rawCapture.truncate(0)
