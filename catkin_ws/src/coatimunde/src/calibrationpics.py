#! /usr/bin/env python

#openCV
import cv2

#open webcam stream
cam = cv2.VideoCapture(0)

#image counter
counter = 0

cv2.namedWindow("Calibration Pictures")

while True:
    ret,frame = cam.read()
    cv2.imshow("Calibration Pictures", frame)
    if not ret:
        break
    k = cv2.waitKey(1)

    if counter > 42:
        break
    elif k%256 == 27:
        #ESC key
        print("Closing")
        break
    elif k%256 == 32:
        img_name = "calibration_frame_{}.jpg".format(counter)
        cv2.imwrite(img_name, frame)
        print("{} written".format(img_name))
        counter += 1
cam.release()
cv2.destroyAllWindows()