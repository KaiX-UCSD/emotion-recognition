import numpy as np
import glob, os, time
import cv2 as cv
from PIL import Image

if __name__ == '__main__':
    
    # initialize face recognizer
    cascade_path = 'haarcascade_frontalface_default.xml'
    face_cascade = cv.CascadeClassifier(cascade_path)
    recognizer = cv.createLBPHFaceRecognizer()
    recognizer.load('trained.xml')

    # initialize camera
    cam = cv.VideoCapture(0)
    face_size = (60,60)
    font = cv.FONT_HERSHEY_SIMPLEX
    print 'Starting ...'
        
    while True:
        ret, frame = cam.read()
        img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(img)    
        for (x,y,w,h) in faces:
            face = img[y:y+h, x:x+w]
            face = cv.resize(img,face_size)
            label_pred, conf = recognizer.predict(face)
            if label_pred == 3 and conf > 70:
                text = 'Eric'
            else:
                text = '?'
            print '{} is correctly recognized with confidence {}.'.format(text, conf)
        for (x,y,w,h) in faces:
            cv.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            cv.putText(frame, text, (x,y), font, 1, (0,255,0), 2)
        cv.imshow('Output', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break


