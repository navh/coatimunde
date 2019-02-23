#! /usr/bin/env python

#python libs
from __future__ import division 
import sys, time

#numpy and scipy
import numpy as np
from scipy.ndimage import filters

from matplotlib import pyplot as plt

#Everything we need to do quaternion math
from tf.transformations import *

#openCV
import cv2
import cv2.aruco as aruco

#ros libraries
import roslib
import rospy

#ros messages
from sensor_msgs.msg import CompressedImage
from coatimunde.msg import MarkerCoords
from coatimunde.msg import PointCoords
from geometry_msgs.msg import QuaternionStamped, Quaternion



VERBOSE=False
PUBLISH_IMAGE = False
depth_channel = '/camera/depth/image_raw/compressedDepth'
target_channel = 'coati/target/output'


class coati_depth:

    def __init__(self):
        #This is where we will store the most recent depth array
        self.depth_arr = []

        #this is where we publish the output
        if PUBLISH_IMAGE:
            self.depth_pub = rospy.Publisher('/output/depth/compressed', CompressedImage, queue_size = 2)
        self.marker_pub = rospy.Publisher('/coati/depth/output/marker', QuaternionStamped, queue_size = 10)
        self.point_pub = rospy.Publisher('/coati/depth/output/point', Quaternion, queue_size = 10)

        #this is where we read from the robot
        self.depth_subscriber = rospy.Subscriber(depth_channel, CompressedImage, self.depth_callback, queue_size=5)
        self.target_subscriber = rospy.Subscriber(target_channel,MarkerCoords, self.target_callback,queue_size=10)
        if VERBOSE:
            print 'subscribed to ' + depth_channel
            print 'subscribed to ' + target_channel

    def depth_callback(self, ros_data):
        lengthOfHeader = 12 #This is a result of the way that depth data is stored in a ros message, the number 12 is sacred
        raw_data = ros_data.data[lengthOfHeader:]
        np_arr = np.fromstring(raw_data, np.uint8)
        self.depth_arr = cv2.imdecode(np_arr,cv2.IMREAD_ANYDEPTH)

        height,width = self.depth_arr.shape[:2]
        distanceAtCentre = self.depth_arr[height//2][width//2]
        
        if distanceAtCentre > 10:
            
            msg = Quaternion()
            msg.x = 0
            msg.y = 0
            msg.z = 0
            msg.w = distanceAtCentre / 1000 #to turn this into meters
            self.point_pub.publish(msg)

        if VERBOSE:
            print 'received depth of type: "%s"' % ros_data.format
        
        if PUBLISH_IMAGE:
            normalizedImg = None
            normalizedImg = cv2.normalize(self.depth_arr, normalizedImg, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC3)
            histogram = cv2.applyColorMap(normalizedImg, cv2.COLORMAP_RAINBOW)

            # create a compressed image
            msg = CompressedImage()
            msg.header.stamp = rospy.Time.now()
            msg.format = 'jpeg'
            msg.data = np.array(cv2.imencode('.jpg', histogram)[1]).tostring()
            # publish that image
            self.depth_pub.publish(msg)

    def target_callback(self, ros_data):
        if len(self.depth_arr) > 0:
            x,y,id = ros_data.x,ros_data.y,ros_data.id
            
            ##THIS IS A BIG STOPGAP MEASURE UNTIL WE ARE ABLE TO MEASUZRE SOME FORM OF AN ANGLE
            #TODO: Fix this silly way to only accept certain things
            height, width = self.depth_arr.shape[:2]
            if x > ((width//2) - 42) and x < ((width//2) + 42):
                distance = self.depth_arr[y][x] / 1000 #To turn it into meters, assuming things are millimeters
                #Consider turning this into a quatrenarion, then it must be published to the map pfinder thing
                if VERBOSE:
                    print 'Marker ' + str(id) + ' is ' + str(distance) + 'm away'
                if distance > 10: #When things are spotted on edges they get weird
                    msg = QuaternionStamped()
                    msg.header.frame_id = str(id)
                    msg.quaternion.x = 0
                    msg.quaternion.y = 0
                    msg.quaternion.z = (x - width//2)/666 ### HOLY COW THIS ONE HAS BEEN MADE MESSY JUST FOR SAKE OF SCIENCE
                    msg.quaternion.w = distance
                    self.marker_pub.publish(msg)

            
def main(args):
    rospy.init_node('coati_depth', anonymous=True)
    cd = coati_depth()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS Coatimunde Depth module"
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
