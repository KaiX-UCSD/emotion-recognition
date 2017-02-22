import numpy as np
import glob, os, time
import cv2 as cv
"""
FRAME_WIDTH = 640 
FRAME_HEIGHT = 480
"""
FRAME_WIDTH = 320
FRAME_HEIGHT = 240

# initialize face recognizer
cascade_path = 'haarcascade_frontalface_default.xml'
face_cascade = cv.CascadeClassifier(cascade_path)
recognizer = cv.createEigenFaceRecognizer()
recognizer.load('trained.xml')

# initialize camera
cam = cv.VideoCapture(0)
cam.set(cv.cv.CV_CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cam.set(cv.cv.CV_CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
face_size = (200,200)
font = cv.FONT_HERSHEY_SIMPLEX

def get_faces_and_label(frame):
    # Convert to gray scale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30) 
    )   

    text = '?'    
    # Recognize face and extract label    
    for (x,y,w,h) in faces:
        face = gray[y:y+h, x:x+w]
        face = cv.resize(face,face_size)
        label_pred, conf = recognizer.predict(face)
        minConfLevel = 2000
        # might need to adjust conf level for higher accuracy 
        if label_pred == 1 and conf > minConfLevel:   
            text = 'Eric' # Eric's ID is 3
 
        # Add on more elif statements like below to include in recognition
        elif label_pred == 7 and conf > minConfLevel:
            text = 'Ducky'

        else:
            text = '?' 
        print '{} is correctly recognized with confidence {}.'.format(text, conf)

    return faces, text

def mark_face(frame, num):

    faces = get_faces(frame)
    # Draw rectangle around faces
    for (x, y, w, h) in faces:
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

if __name__ == '__main__':
    
    print 'Starting ...'
        
    while True:
        ret, frame = cam.read()
        frame = cv.flip(frame, 1)

        faces, text = get_faces_and_label(frame)

        # Display frame with label
        for (x,y,w,h) in faces:
            cv.rectangle(frame, (x,y), (x + w, y + h), (0, 255, 0), 2)
            cv.putText(frame, text, (x,y), font, 1, (0, 255, 0), 2)
        cv.imshow('Output', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv.destroyAllWindows()
