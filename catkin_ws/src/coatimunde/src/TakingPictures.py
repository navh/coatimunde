#! /usr/bin/env python

#python libs
import sys, time

#numpy and scipy
import numpy as np
from scipy.ndimage import filters

from matplotlib import pyplot as plt

#openCV
import cv2
import time

#ros libraries
import roslib
import rospy

#ros messages
from sensor_msgs.msg import CompressedImage




#some nasty globals
VERBOSE=True


class aruco_tracker:

    def __init__(self):

        self.counter = 60
        self.delay = 0
        self.gray = None
        #this is where we read from the robot
        self.subscriber = rospy.Subscriber('/camera/rgb/image_raw/compressed',CompressedImage, self.callback, queue_size=5)

    def callback(self, ros_data):

        np_arr = np.fromstring(ros_data.data, np.uint8)
        image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR) #second argument should be cv2.IMREAD_COLOR for OpenCV >= 3.0
        self.gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        if self.delay>100:
            self.delay = 0
            self.saving()
        self.delay +=1



    def saving(self):

        if self.counter < 100:
            img_name = 'calibration_frame_{}.jpg'.format(self.counter)
            path = '/home/t/calibration_photos/'
            cv2.imwrite(str(path) + img_name, self.gray)
            print("{} written".format(img_name))
            self.counter += 1
        #/home/t/calibration_photos




def main(args):
    ac = aruco_tracker()
    rospy.init_node('coati_target', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down ROS Coatimunde Target Identifier module")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
