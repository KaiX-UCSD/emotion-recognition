import numpy as np
import glob, os, time
import cv2 as cv

if __name__ == '__main__':
    
    # initialize face recognizer
    cascade_path = 'haarcascade_frontalface_default.xml'
    face_cascade = cv.CascadeClassifier(cascade_path)
    recognizer = cv.createLBPHFaceRecognizer()
    recognizer.load('trained.xml')

    # initialize camera
    cam = cv.VideoCapture(0)
    face_size = (70,70)
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

            # might need to adjust conf level for higher accuracy 
            if label_pred == 3 and conf > 80:   
                text = 'Eric' # Eric's ID is 3
            
            # Add on more elif statements like below to include in recognition
            elif label_pred == 10 and conf > 80:
                text = 'Tom'

            else:
                text = '?'
            print '{} is correctly recognized with confidence {}.'.format(text, conf)
        for (x,y,w,h) in faces:
            cv.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            cv.putText(frame, text, (x,y), font, 1, (0,255,0), 2)
        cv.imshow('Output', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break


