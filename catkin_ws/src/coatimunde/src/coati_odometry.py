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
from geometry_msgs.msg import Twist

#some nasty globals
VERBOSE=True

class aruco_tracker:

    def __init__(self):
        pass

    def callback(self, ros_data):
        pass

def main(args):
    ac = aruco_tracker()
    rospy.init_node('coati_odometry', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS Coatimunde Odometry module"
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
