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
from geometry_msgs.msg import Twist
from geometry_msgs.msg import QuaternionStamped, Quaternion


#some nasty globals
VERBOSE=True
MOVEMENT_ENABLED=True
NUMBER_OF_POINTS_TO_REMEMBER = 1234

#very bad list thing created just to watch this guy bounce between targets
#good lord kara why did you choose such terrible numbers... who cares if the markers look cool, this is just awkward to deal with now
GOAL = [197,151,134,25,205,167,134,25]


class coati_pfinder:

    def __init__(self):

        self.locationCounter = 0

        self.targets = {} #Dictionary will be used to keep track of targets to associate ids with locations
        self.points = []

        # Subscribe to both target and point things maybe
        #self.target_sub = rospy.Subscriber('coati/target/output', MarkerCoords, self.marker_callback, queue_size = 10)

        self.odom_sub = rospy.Subscriber('/coati/odometry/output', Quaternion, self.odom_callback, queue_size = 10)
        self.marker_sub = rospy.Subscriber('/coati/depth/output/marker', QuaternionStamped, self.marker_callback, queue_size=10)
        self.point_sub = rospy.Subscriber('/coati/depth/output/point', Quaternion, self.point_callback, queue_size=10)

        # Send movement commands to some generic ros vehicle
        self.velo_pub = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size = 10)

        r = rospy.Rate(10)  # 10hz, as per our specifications
        while not rospy.is_shutdown():
            self.take_movement_decision()
            r.sleep()



    def marker_callback(self, ros_data):
        key = int(ros_data.header.frame_id)
        x = ros_data.quaternion.x
        y = ros_data.quaternion.y
        z = ros_data.quaternion.z
        w = ros_data.quaternion.w
        self.targets[key] = ([x,y,z,w])
        if VERBOSE:
            pass
            #print 'Target ' + str(key) + ' updated to ' + str(self.targets[key])

    def point_callback(self, ros_data):
        if len(self.points) >= NUMBER_OF_POINTS_TO_REMEMBER: #I think this needs to change, instead lets half it if it takes too long
            del self.points[0]
        x = ros_data.x
        y = ros_data.y
        z = ros_data.z
        w = ros_data.w
        self.points.append([x,y,z,w])

    def odom_callback(self,ros_data):
        x = ros_data.x
        y = ros_data.y
        z = ros_data.z
        w = ros_data.w
        transform = [x,y,z,-w] # Negative W component does the inverse of the motion of the robot
        for key, vector in self.targets.items():
            self.targets[key] = quaternion_multiply(transform,vector) # Multiply does not do what you think it does, it actually multiplies them... to add them you just want to multiply them. Figure that out.
        for i in xrange(len(self.points)):
            self.points[i] = quaternion_multiply(transform,self.points[i])

    def take_movement_decision(self):
        # create a movement message, this needs to be in its own little world

        move_cmd = Twist()

        if GOAL[self.locationCounter] in self.targets:
            print 'Spotted target ' + str(GOAL[self.locationCounter]) + ' which is ' + str(self.targets[GOAL[self.locationCounter]]) + 'm away.'
            if self.targets[GOAL[self.locationCounter]][2] > 0:
                move_cmd.angular.z = -0.1
            else:
                move_cmd.angular.z = 0.1
            move_cmd.linear.x = 0.3
            if self.targets[GOAL[self.locationCounter]][3] < 1:
                print 'Next target'
                self.locationCounter = ((self.locationCounter + 1) % len(GOAL)) #Hopefully this causes it to do the circuit
        else:
            move_cmd.angular.z = -0.3

        for thing in self.targets:
            print str(thing) + str(self.targets[thing])

        self.velo_pub.publish(move_cmd)



def main(args):
    rospy.init_node('coati_pfinder', anonymous=True)
    pfinder = coati_pfinder()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS Coatimunde Pfinder module"
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
