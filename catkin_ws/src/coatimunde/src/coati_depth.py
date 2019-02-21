#! /usr/bin/env python

#python libs
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
from coatimunde.msg import MarkerCoords
from coatimunde.msg import PointCoords


VERBOSE=False
PUBLISH_IMAGE = True
depth_channel = '/camera/depth/image_raw/compressedDepth'
target_channel = 'coati_target/output'

class aruco_tracker:

    def __init__(self):
        #This is where we will store the most recent depth array
        self.depth_arr = None

        #this is where we publish the output
        if PUBLISH_IMAGE:
            self.depth_pub = rospy.Publisher("/output/depth/compressed", CompressedImage, queue_size = 2)

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
        x,y,id = ros_data.x,ros_data.y,ros_data.id
        distance = self.depth_arr[y][x]
        #Consider turning this into a quatrenarion, then it must be published to the map pfinder thing
        print 'Marker ' + str(id) + ' is ' + str(distance) + 'mm away'
            
def main(args):
    ac = aruco_tracker()
    rospy.init_node('coati_depth', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS Coatimunde Depth module"
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
