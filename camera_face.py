import cv2
import numpy as np
import os 
import time
from base_camera import BaseCamera
from mail import sendemail

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
last_send = 0
font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

# names related to ids
names = ['None', '', '']

class Camera(BaseCamera): 
    video_source = 0

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source
    @staticmethod
    def frames():
        # Initialize and start realtime video capture
        cam = cv2.VideoCapture(Camera.video_source)
        cam.set(3, 640) # set video widht
        cam.set(4, 480) # set video height
        if not cam.isOpened():
            raise RuntimeError('Could not start camera.')

        # Define min window size to be recognized as a face
        minW = 0.1*cam.get(3)
        minH = 0.1*cam.get(4)

        while True:
            global last_send
            ret, img =cam.read()
            img = cv2.flip(img, -1) # Flip vertically

            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale( 
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (int(minW), int(minH)),
               )

            for(x,y,w,h) in faces:

                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

                id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

                # Check if confidence is less them 100 -> "0" is perfect match 
                if (confidence < 85):
                    id = names[id]
                    confidence = "  {0}%".format(round(100 - confidence))
                else:
                    id = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))
                    try:
                        if(time.time() - last_send) > 30:
                            last_send = time.time()
                            print ("Sending email...")
                            sendemail()
                            print ("done!")
                    except:
                        print ("Error sending email!")
        
                cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
                cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()
