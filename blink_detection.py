import numpy as np
import cv2

def eye_detection(img, face_cascade, eye_cascade):
  eye_open = 'open'

  #Coverting the recorded image to grayscale
  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  #Applying filter to remove impurities
  gray = cv2.bilateralFilter(gray,5,1,1)
  #Detecting the face for region of image to be fed to eye classifier
  faces = face_cascade.detectMultiScale(gray, 1.3, 5,minSize=(200,200))

  if(len(faces)>0):
    for (x,y,w,h) in faces:
      img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),4)
      
      #roi_face is face which is input to eye classifier
      roi_face = gray[y:y+h,x:x+w]
      roi_face_clr = img[y:y+h,x:x+w]
      eyes = eye_cascade.detectMultiScale(roi_face,1.3,5,minSize=(50,50))
      
      #Examining the length of eyes object for eyes
      if(len(eyes)>=2):
          cv2.putText(img, "eyes open", (70,70), cv2.FONT_HERSHEY_PLAIN, 1.5, (159,50,0),2)
      else: 
        cv2.putText(img, "eyes closed", (70,70), cv2.FONT_HERSHEY_PLAIN, 1.5, (50,159,255),2)
        eye_open = 'close'
  else:
    cv2.putText(img,"no face detected",(100,100),cv2.FONT_HERSHEY_PLAIN, 1.5, (255,255,255),2)

  # add filter to image
  img = inc_brightness(img)
  return eye_open, img


def face_detection(img, face_cascade):
  watched = False

  #Coverting the recorded image to grayscale
  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  #Applying filter to remove impurities
  gray = cv2.bilateralFilter(gray,5,1,1)
  #Detecting the face for region of image to be fed to eye classifier
  faces = face_cascade.detectMultiScale(gray, 1.3, 5,minSize=(200,200))

  if(len(faces)>0):
    for (x,y,w,h) in faces:
      img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),4)
    cv2.putText(img, "watched", (70,70), cv2.FONT_HERSHEY_PLAIN, 1.5, (50,159,255),2)
    watched = True
  else:
    cv2.putText(img,"not watched",(100,100),cv2.FONT_HERSHEY_PLAIN, 1.5, (255,255,255),2)
    watched = False

  # add filter to image
  img = inc_brightness(img)
  return watched, img


def inc_brightness(img):
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  h, s, v = cv2.split(hsv)

  added_brightness = 50
  lim = 255 - added_brightness
  v[v > lim] = 255
  v[v <= lim] += added_brightness
  
  lowered_saturation = 100
  s[s > lowered_saturation] -= lowered_saturation
  s[s <= lowered_saturation] = 0

  final_hsv = cv2.merge((h, s, v))
  img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
  return img
