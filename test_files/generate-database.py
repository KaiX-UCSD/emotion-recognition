import numpy as np
import cv2 as cv
import os
from PIL import Image

# Initialize webcam
cap = cv.VideoCapture(0)

# For face detection we will use the Haar Cascade provided by OpenCV
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
        minNeighbors=5,
        minSize=(30, 30)
    )
    #cv.imwrite('test.jpg', faces)
    return faces

def mark_face(frame, num):

    faces = get_faces(frame)
    # Draw rectangle around faces
    for (x, y, w, h) in faces:
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cropFrame = frame[y: y+h, x: x+w]
	name = "frame%d.jpg"%num
	cv.imwrite(name, cropFrame)

def get_images_and_labels(path, name):
    # Append all the absolute image paths in a list image_paths
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    # images will contains face images
    images = []
    # labels will contains the label that is assigned to the image
    labels = []
    for image_path in image_paths:
        # Read the image and convert to grayscale
        image_pil = Image.open(image_path).convert('L')
        # Convert the image format into numpy array
        image = np.array(image_pil, 'uint8')
        # Get the label of the image
        nbr = int(os.path.split(image_path)[1].split("_")[0].replace(name,""))
        # Detect the face in the image
        faces = faceCascade.detectMultiScale(image)
        # If face is detected, append the face to images and the label to labels
        for (x, y, w, h) in faces:
            images.append(image[y: y + h, x: x + w]) 
            labels.append(nbr)
            cv.imshow("Adding faces to traning set...", image[y: y + h, x: x + w]) 
            cv.waitKey(50)
    # return the images list and labels list
    return images, labels



# counter for saving images
imgNum = 0   
# create a new folder to store images
name = raw_input('What is your name? ')
dirname = name + 'database'
os.mkdir(dirname)
print 'Press any key to take picture'
# ID for associated person 
numID = '01'
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Processing
#    mark_face(frame, frameNum)

    # Display the resulting frame
    cv.imshow('frame', frame)
    # Wait for 1 ms for user to hit any key
    delay = cv.waitKey(1)
    if delay != -1:
        cv.imwrite(os.path.join(dirname, name+numID+'_'+str(imgNum)+'.jpg'), frame)
        imgNum += 1 
        print 'Picture taken!' 
    elif imgNum == 10:
        break

print 'Database for '+name+' created'

# Release capture
cap.release()
cv.destroyAllWindows()

# Path to the image database
path = os.path.join('.', dirname)

# load the images and lables
images, labels = get_images_and_labels(path, name)

# Perfrom training and save to xml file
recognizer = cv.createLBPHFaceRecognizer()
recognizer.train(images, np.array(labels))
recognizer.save(name+'_trained.xml')
print 'xml file for '+name+' created!'


