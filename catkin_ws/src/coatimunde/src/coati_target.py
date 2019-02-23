#! /usr/bin/env python

#python libs
from __future__ import division 
import sys, time

#numpy and scipy
import numpy as np
from scipy.ndimage import filters

from matplotlib import pyplot as plt

#openCV
import cv2
import cv2.aruco as aruco

#ros libraries
import roslib
import rospy

#ros messages
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import Twist
from coatimunde.msg import MarkerCoords
from coatimunde.msg import PointCoords

#some nasty globals
font = cv2.FONT_HERSHEY_SIMPLEX
VERBOSE=True
VERSION_TEXT= 'v0.2-'
PUBLISH_IMAGE = True
aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
parameters = aruco.DetectorParameters_create()


class coati_target:

    def __init__(self):

        #this is where we publish the output
        if PUBLISH_IMAGE:
            self.image_pub = rospy.Publisher("/output/image_raw/compressed", CompressedImage, queue_size = 1)
        self.marker_pub = rospy.Publisher('coati/target/output', MarkerCoords, queue_size = 5)

        #this is where we read from the robot
        self.subscriber = rospy.Subscriber('/camera/rgb/image_raw/compressed',CompressedImage, self.callback, queue_size=5)

    def callback(self, ros_data):

        outputText = VERSION_TEXT

        if VERBOSE:
            print 'received image of type: "%s"' % ros_data.format

        np_arr = np.fromstring(ros_data.data, np.uint8)
        image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR) #second argument should be cv2.IMREAD_COLOR for OpenCV >= 3.0
        gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

        #The actual act of parsing out the marker info
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        if np.all(ids != None):

            if PUBLISH_IMAGE:
                outputText += 'Found:'
                aruco.drawDetectedMarkers(image_np,corners)

            for i in range(0, ids.size):
                if int(ids[i][0]) != 0:
                    outputText += str(ids[i][0]) + ', '

                    # Find the center of the marker
                    cX = int((corners[i][0][0][0] + corners[i][0][1][0]) / 2)
                    cY = int((corners[i][0][0][1] + corners[i][0][2][1]) / 2)

                    # ids[i][0] <- this is the id name that I want to use for the dict
                    msg = MarkerCoords()
                    msg.x = cX
                    msg.y = cY
                    msg.id = int(ids[i][0])
                    self.marker_pub.publish(msg)

        else:
            if PUBLISH_IMAGE:
                outputText += 'No Marker'

        if PUBLISH_IMAGE:
            #Display what was found, marker and its number or no marker
            cv2.putText(image_np, (outputText), (32, 32), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

            #create a compressed image
            msg = CompressedImage()
            msg.header.stamp = rospy.Time.now()
            msg.format = 'jpeg'
            msg.data = np.array(cv2.imencode('.jpg',image_np) [1]).tostring()
            #publish that image
            self.image_pub.publish(msg)

def main(args):
    rospy.init_node('coati_target', anonymous=True)
    ct = coati_target()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS Coatimunde Target Identifier module"
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
