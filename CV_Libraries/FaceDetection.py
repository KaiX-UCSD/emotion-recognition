import numpy as np
import cv2 as cv
import time

class FaceDetection:
    def __init__(self, debug=True, onComputer=True,cascPath='../cascades/haarcascade_frontalface_default.xml'):
        self.debug = debug
        self.onComputer = onComputer
        self.FRAME_WIDTH = 320
        self.FRAME_HEIGHT = 240

        if not self.onComputer:
            from CamControl import CamControl
            self.camera = CamControl()
            self.camera.up(50, 9)
        # Create haar cascade
        self.faceCascade = cv.CascadeClassifier(cascPath)

    # Detect faces from image and return an array of faces
    # @return faces - an array of tuples (x,y,w,h)
    def get_faces(self,frame):
        # Convert to gray scale
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Detect faces
        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(50, 50)
        )
        return faces

    # Draw boxes around faces
    # @return none
    def mark_face(self,frame, faces):
        # Draw rectangle around faces
        for (x, y, w, h) in faces:
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv.circle(frame, (x+w/2, y+h/2), 1, (0, 0, 255), 2)

    # Determine center of a defined face.
    # Input: face - [x, y, w, h] of top right of the face
    # Return the [x_center,y_center] center of the face in the frame
    def center_face(self,face):
        (xFace, yFace, wFace, hFace) = face

        # return center of face
        return [(wFace / 2 + xFace), (hFace / 2 + yFace)]


    def face_detect(self, frame):
        faces = self.get_faces(frame)
        self.mark_face(frame,faces)
        # when a face is detected. Return the frame.
        if( len(faces) != 0):
            self.move_camera(faces)
            return frame
        else:
            return None
    """
    move_camera() 
    @param cFace is coordinates to the center of the faces - [X, Y]
    """
    def move_camera(self, faces):        
        if len(faces) == 0:
            return
        cFace = self.center_face(faces[0])
        if cFace[0] > self.FRAME_WIDTH / 2 + 40:
            if not self.onComputer:
                self.camera.left(9, 3)
            else:
                print "left"
        elif cFace[0] > self.FRAME_WIDTH / 2 + 30:
            if not self.onComputer:
                self.camera.left(7, 2)
            else:
                print "left"
        elif cFace[0] > self.FRAME_WIDTH / 2 + 20:
            if not self.onComputer:
                self.camera.left(5, 1)
            else:
                print "left"

        elif cFace[0] < self.FRAME_WIDTH / 2 - 40:
            # move left
            if not self.onComputer:
                self.camera.right(9, 3)
            else:
                print "right"
        elif cFace[0] < self.FRAME_WIDTH / 2 - 30:
            # move left
            if not self.onComputer:
                self.camera.right(7, 2)
            else:
                print "right"
        elif cFace[0] < self.FRAME_WIDTH / 2 - 20:
            # move left
            if not self.onComputer:
                self.camera.right(5, 1)
            else:
                print "right"

        if cFace[1] > self.FRAME_HEIGHT / 2 + 40:
            # move down
            if not self.onComputer:
                self.camera.down(9, 3)
            else:
                print "down"
        elif cFace[1] > self.FRAME_HEIGHT / 2 + 30:
            # move down
            if not self.onComputer:
                self.camera.down(7, 2)
            else:
                print "down"
        elif cFace[1] > self.FRAME_HEIGHT / 2 + 20:
            # move down
            if not self.onComputer:
                self.camera.down(5, 1)
            else:
                print "down"

        elif cFace[1] < self.FRAME_HEIGHT / 2 - 40:
            # move up
            if not self.onComputer:
                self.camera.up(9, 3)
            else:
                print "up"
        elif cFace[1] < self.FRAME_HEIGHT / 2 - 30:
            # move up
            if not self.onComputer:
                self.camera.up(7, 2)
            else:
                print "up"
        elif cFace[1] < self.FRAME_HEIGHT / 2 - 20:
            # move up
            if not self.onComputer:
                self.camera.up(5, 1)
            else:
                print "up"
            


    """
    This script runs to test the face detection software.
    """
    def debugging_script(self, cascPath='../cascades/haarcascade_frontalface_default.xml'):
        #Set dimensions of frame as 320x240 for better performance on Pi
	# self.FRAME_WIDTH = 720
	# self.FRAME_HEIGHT = 480
        cap = cv.VideoCapture(0)
        cap.set(cv.cv.CV_CAP_PROP_FRAME_WIDTH, self.FRAME_WIDTH)
        cap.set(cv.cv.CV_CAP_PROP_FRAME_HEIGHT, self.FRAME_HEIGHT)

        time.sleep(1)
        while True:

            # Capture frame-by-frame
            ret, frame = cap.read()
            cv.flip(frame, 1, frame)  # flip the image

            # ----------------- Image Processing -------------------------#
            # Detect Faces
            faces = self.get_faces(frame)
            cFace = [0,0]
            if len(faces) != 0:
                cFace = self.center_face(faces[0])
            
            # Draw boxes around the faces
            if self.debug:
                self.mark_face(frame, faces)

            if self.debug:
                cv.imshow("View", frame)
            
            if cFace[0] != 0:
                if cFace[0] > self.FRAME_WIDTH / 2 + 40:
                    if not self.onComputer:
                        self.camera.left(9, 3)
                    else:
                        print "left"
                elif cFace[0] > self.FRAME_WIDTH / 2 + 30:
                    if not self.onComputer:
                        self.camera.left(7, 2)
                    else:
                        print "left"
                elif cFace[0] > self.FRAME_WIDTH / 2 + 20:
                    if not self.onComputer:
                        self.camera.left(5, 1)
                    else:
                        print "left"

                elif cFace[0] < self.FRAME_WIDTH / 2 - 40:
                    # move left
                    if not self.onComputer:
                        self.camera.right(9, 3)
                    else:
                        print "right"
                elif cFace[0] < self.FRAME_WIDTH / 2 - 30:
                    # move left
                    if not self.onComputer:
                        self.camera.right(7, 2)
                    else:
                        print "right"
                elif cFace[0] < self.FRAME_WIDTH / 2 - 20:
                    # move left
                    if not self.onComputer:
                        self.camera.right(5, 1)
                    else:
                        print "right"

                if cFace[1] > self.FRAME_HEIGHT / 2 + 40:
                    # move down
                    if not self.onComputer:
                        self.camera.down(9, 3)
                    else:
                        print "down"
                elif cFace[1] > self.FRAME_HEIGHT / 2 + 30:
                    # move down
                    if not self.onComputer:
                        self.camera.down(7, 2)
                    else:
                        print "down"
                elif cFace[1] > self.FRAME_HEIGHT / 2 + 20:
                    # move down
                    if not self.onComputer:
                        self.camera.down(5, 1)
                    else:
                        print "down"

                elif cFace[1] < self.FRAME_HEIGHT / 2 - 40:
                    # move up
                    if not self.onComputer:
                        self.camera.up(9, 3)
                    else:
                        print "up"
                elif cFace[1] < self.FRAME_HEIGHT / 2 - 30:
                    # move up
                    if not self.onComputer:
                        self.camera.up(7, 2)
                    else:
                        print "up"
                elif cFace[1] < self.FRAME_HEIGHT / 2 - 20:
                    # move up
                    if not self.onComputer:
                        self.camera.up(5, 1)
                    else:
                        print "up"
            
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        # Release capture
        cap.release()
        cv.destroyAllWindows()
