import numpy as np
import cv2 as cv

imagePath = 'face1.jpg'
cascPath = 'haarcascade_frontalface_default.xml'

# Create haar cascade
faceCascade = cv.CascadeClassifier(cascPath)

# Read the image in gray scale
image = cv.imread(imagePath)
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

# Detect faces in the image
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30)
)

# Draw rectangles around the face
for (x, y, w, h) in faces:
    cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv.imshow('Faces found', image)
cv.waitKey(0)
cv.destroyAllWindows()
