import numpy as np
from PIL import Image
import os, glob, cv2, time, argparse

face_size = (60,60)

def get_image_paths(path, key):
    img_path = os.path.join(path, key)
    img_path_list = glob.glob(img_path)
    return img_path_list

def get_images_and_labels(face_cascade, path, key):
    img_path_list = get_image_paths(path, key)
    face_list = []
    label_list = []
    for img_path in img_path_list:
        img_name = img_path.split('/')[-1]
        if img_name[0]=='w':
            continue
        label = 2
        #print img_name, img_cate, label
        #label_list.append(label)
        img = cv2.imread(img_path,0)
        #print img.shape
        img = cv2.resize(img, (160,120))
        #cv2.imwrite('s1.jpg', img)
        print img.shape
        faces = face_cascade.detectMultiScale(img)
        #print faces
        for (x,y,w,h) in faces:
            face = img[y:y+h, x:x+w]
            face = cv2.resize(face, face_size)
            print face.shape
            face_list.append(face)
            label_list.append(label)
        #print x, y, w, h, face.shape
        #break
    return face_list, label_list

def train_recognizer(face_cascade):
    print 'reading images'
    t1 = time.time()
    face_list, label_list = get_images_and_labels(face_cascade, 'willfaces', '*jpg')
    t2 = time.time()
    print 'Time for reading images and labels:', t2-t1
    print 'list length:', len(face_list), len(label_list)
    #print label_list
    
    recognizer = cv2.createEigenFaceRecognizer()
    t1 = time.time()
    recognizer.train(face_list, np.array(label_list))
    recognizer.save('willface.xml')
    t2 = time.time()
    print 'Time for training the recognizer:', t2-t1
    print 'training complete'

def load_recognizer(file):
    recognizer = cv2.createEigenFaceRecognizer()
    t1 = time.time()
    recognizer.load(file)
    t2 = time.time()
    print 'Time for loading recognizer:', t2-t1
    print 'loading complete'
    return recognizer
    

if __name__ == '__main__':

    
    
    
    cascade_path = 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)

    #train_recognizer(face_cascade)
    
    #'''
    recognizer = load_recognizer('willface.xml')
    t1 = time.time()
    img_path_list = get_image_paths('willfaces', '*.jpg')
    for img_path in img_path_list:
        img_name = img_path.split('/')[-1]
        '''
        if img_name[0] != 'w':
            continue
        '''
        label_real = 2
        img = cv2.imread(img_path,0)
        #print img.shape
        img = cv2.resize(img, (160,120))
        #cv2.imwrite('s1.jpg', img)
        #print img.shape
        faces = face_cascade.detectMultiScale(img)
        #print faces
        for (x,y,w,h) in faces:
            face = img[y:y+h, x:x+w]
            face = cv2.resize(face, face_size)
            label_pred, conf = recognizer.predict(face)
            if label_pred == label_real:
                print '{} is correctly recognized with confidence {}.'.format(label_real, conf)
            else:
                print '{} wrong as {}.'.format(label_full, label_pred)
    t2 = time.time()
    print 'Time for image recognition:', t2-t1
    #'''
