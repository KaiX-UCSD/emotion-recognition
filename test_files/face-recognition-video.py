import numpy as np
import cv2 as cv

FRAME_WIDTH = 320
FRAME_HEIGHT = 240
cap = cv.VideoCapture(0)
cap.set(cv.cv.CV_CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv.cv.CV_CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

cascPath = '../cascades/haarcascade_frontalface_default.xml'

# Create haar cascade
faceCascade = cv.CascadeClassifier(cascPath)


def get_faces(frame):
    # Convert to gray scale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Detect faces
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=1,
        minSize=(30, 30)
    )
    return faces


def mark_face(frame):

    faces = get_faces(frame)
    # Draw rectangle around faces
    for (x, y, w, h) in faces:
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Processing
    mark_face(frame)

    # Display the resulting frame
    cv.imshow('frame', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Release capture
cap.release()
cv.destroyAllWindows()
