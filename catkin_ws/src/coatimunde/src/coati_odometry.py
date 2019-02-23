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
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Twist

#some nasty globals
VERBOSE=True

class coati_odometry:

    def __init__(self):

        # this first one will probably be wrong, but I'm really not sure how else t odo
        self.thyme = rospy.Time.now()
        
        # subscribe to the geo msg transforms
        self.transform_sub = rospy.Subscriber('/odom', Odometry, self.callback, queue_size = 10)

        # publish to this channel and let pfinder take care of applying these transformations
        self.odom_out = rospy.Publisher('/coati/odometry/output', Quaternion, queue_size = 10)
        if VERBOSE:
            print ('Done the init')

    def callback(self, ros_data):

        delta = (ros_data.header.stamp - self.thyme).to_sec() # time from the last packet analyzed and this one we calculated, this lets us drop some messages and just interpolate the middle bits
        self.thyme = ros_data.header.stamp

        doubleyou = (ros_data.twist.twist.linear.x * ros_data.twist.twist.linear.x + ros_data.twist.twist.linear.y * ros_data.twist.twist.linear.y + ros_data.twist.twist.linear.z * ros_data.twist.twist.linear.z) ** 2

        msg = Quaternion()
        msg.x = delta * ros_data.twist.twist.angular.x
        msg.y = delta * ros_data.twist.twist.angular.y
        msg.z = delta * ros_data.twist.twist.angular.z
        msg.w = delta * doubleyou
        if VERBOSE:
            print(msg)
        self.odom_out.publish(msg)

        # Maybe if this thing packages up many of these and makes a single bigger vector that the other process can pull
        # whenever it is needed would prevent the next thing from being overwhelmed with many tiny changes

def main(args):
    rospy.init_node('coati_odometry', anonymous=True)
    co = coati_odometry()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS Coatimunde Odometry module"
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
