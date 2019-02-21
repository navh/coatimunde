#! /usr/bin/env python

import numpy as np
import cv2
import glob

#criteria set, the size of each chessboard square goes in here
crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

#prepare object points and matrix
object = np.zeros((6*8,3), np.float32)
object[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)

#Arrays to store image points and object points from the images
objectpoints = []
imagepoints = []

images = glob.glob('*.jpg') #Getting the images from the folder

for fname in images:
    image = cv2.imread(fname)
    grey = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    #find the corners of the chessboard
    ret, corners = cv2.findChessboardCorners(grey, (8,6))

    #if found then add the pretty lines and add to arrays
    if ret == True:
        objectpoints.append(object)
        corners2 = cv2.cornerSubPix(grey,corners,(11,11),(-1,-1),crit)
        imagepoints.append(corners2)

        #draw and display the corners
        image = cv2.drawChessboardCorners(image, (8,6), corners2,ret)
        cv2.imshow('image', image)
        cv2.waitKey(500)
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objectpoints, imagepoints, grey.shape[::-1])

cv2.destroyAllWindows()

