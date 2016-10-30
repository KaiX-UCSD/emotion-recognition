import numpy as np
import cv2 as cv
import time

FRAME_WIDTH = 320
FRAME_HEIGHT = 240
cap = cv.VideoCapture(0)
cap.set(cv.cv.CV_CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv.cv.CV_CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

cascPath = 'haarcascade_frontalface_default.xml'

# Create haar cascade
faceCascade = cv.CascadeClassifier(cascPath)


def get_faces(frame):
    # Convert to gray scale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Detect faces
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    return faces


def mark_face(frame):
    faces = get_faces(frame)

    # Ghetto tricK: store the w,h,x,y values of last face
    xFace = 0
    yFace = 0
    wFace = 0
    hFace = 0

    # Draw rectangle around faces
    for (x, y, w, h) in faces:
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        xFace = x
        yFace = y
        wFace = w
        hFace = h

    # return center of face
    return [(wFace / 2 + xFace), (hFace / 2 + yFace)]


from CamControl import CamControl

camera = CamControl()
camera.up(50, 9)
time.sleep(1)
while True:

    # Capture frame-by-frame
    ret, frame = cap.read()
    ret, frame = cap.read()
    ret, frame = cap.read()
    ret, frame = cap.read()
    ret, frame = cap.read()
    cv.flip(frame, 1, frame)  # flip the image

    # Processing
    # faces = get_faces(frame)
    # faces = 0
    # Display the resulting frame
    cFace = mark_face(frame)
    cv.imshow("View", frame)

    if cFace[0] != 0:

        if cFace[0] > FRAME_WIDTH / 2 + 40:
            camera.left(9, 3)
        elif cFace[0] > FRAME_WIDTH / 2 + 30:
            camera.left(7, 2)
        elif cFace[0] > FRAME_WIDTH / 2 + 20:
            camera.left(5, 1)

        elif cFace[0] < FRAME_WIDTH / 2 - 40:
            # move left
            camera.right(9, 3)
        elif cFace[0] < FRAME_WIDTH / 2 - 30:
            # move left
            camera.right(7, 2)
        elif cFace[0] < FRAME_WIDTH / 2 - 20:
            # move left
            camera.right(5, 1)

        if cFace[1] > FRAME_HEIGHT / 2 + 40:
            # move down
            camera.down(9, 3)
        elif cFace[1] > FRAME_HEIGHT / 2 + 30:
            # move down
            camera.down(7, 2)
        elif cFace[1] > FRAME_HEIGHT / 2 + 20:
            # move down
            camera.down(5, 1)

        elif cFace[1] < FRAME_HEIGHT / 2 - 40:
            # move up
            camera.up(9, 3)
        elif cFace[1] < FRAME_HEIGHT / 2 - 30:
            # move up
            camera.up(7, 2)
        elif cFace[1] < FRAME_HEIGHT / 2 - 20:
            # move up
            camera.up(5, 1)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Release capture
cap.release()
cv.destroyAllWindows()
