import numpy as np
import cv2 as cv
import time

debug = True
onComputer = True

#Set dimensions of frame as 320x240 for better performance on Pi
FRAME_WIDTH = 320
FRAME_HEIGHT = 240
cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

cascPath = 'haarcascade_frontalface_default.xml'

# Create haar cascade
faceCascade = cv.CascadeClassifier(cascPath)

# Detect faces from image and return an array.
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

# Draw boxes around faces
def mark_face(frame, faces):
    # Draw rectangle around faces
    for (x, y, w, h) in faces:
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv.circle(frame, (x+w/2, y+h/2), 1, (0, 0, 255), 2)

# Determine center of a defined face.
# Input: face - [x, y, w, h] of top right of the face
# Return the [x_center,y_center] center of the face in the frame
def center_face(face):
    (xFace, yFace, wFace, hFace) = face

    # return center of face
    return [(wFace / 2 + xFace), (hFace / 2 + yFace)]


from CamControl import CamControl

if not onComputer:
    camera = CamControl()
    camera.up(50, 9)

    
time.sleep(1)
while True:

    # Capture frame-by-frame
    ret, frame = cap.read()
    cv.flip(frame, 1, frame)  # flip the image

    # ----------------- Image Processing -------------------------#
    # Detect Faces
    faces = get_faces(frame)
    cFace = [0,0]
    if len(faces) != 0:
        cFace = center_face(faces[0])
    
    # Draw boxes around the faces
    if debug:
        mark_face(frame, faces)

    if debug:
        cv.imshow("View", frame)
    
    if cFace[0] != 0:
        if cFace[0] > FRAME_WIDTH / 2 + 40:
            if not onComputer:
                camera.left(9, 3)
            else:
                print "left"
        elif cFace[0] > FRAME_WIDTH / 2 + 30:
            if not onComputer:
                camera.left(7, 2)
            else:
                print "left"
        elif cFace[0] > FRAME_WIDTH / 2 + 20:
            if not onComputer:
                camera.left(5, 1)
            else:
                print "left"

        elif cFace[0] < FRAME_WIDTH / 2 - 40:
            # move left
            if not onComputer:
                camera.right(9, 3)
            else:
                print "right"
        elif cFace[0] < FRAME_WIDTH / 2 - 30:
            # move left
            if not onComputer:
                camera.right(7, 2)
            else:
                print "right"
        elif cFace[0] < FRAME_WIDTH / 2 - 20:
            # move left
            if not onComputer:
                camera.right(5, 1)
            else:
                print "right"

        if cFace[1] > FRAME_HEIGHT / 2 + 40:
            # move down
            if not onComputer:
                camera.down(9, 3)
            else:
                print "down"
        elif cFace[1] > FRAME_HEIGHT / 2 + 30:
            # move down
            if not onComputer:
                camera.down(7, 2)
            else:
                print "down"
        elif cFace[1] > FRAME_HEIGHT / 2 + 20:
            # move down
            if not onComputer:
                camera.down(5, 1)
            else:
                print "down"

        elif cFace[1] < FRAME_HEIGHT / 2 - 40:
            # move up
            if not onComputer:
                camera.up(9, 3)
            else:
                print "up"
        elif cFace[1] < FRAME_HEIGHT / 2 - 30:
            # move up
            if not onComputer:
                camera.up(7, 2)
            else:
                print "up"
        elif cFace[1] < FRAME_HEIGHT / 2 - 20:
            # move up
            if not onComputer:
                camera.up(5, 1)
            else:
                print "up"
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Release capture
cap.release()
cv.destroyAllWindows()
