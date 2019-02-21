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
font = cv2.FONT_HERSHEY_SIMPLEX
versionString = 'v0.1-'
VERBOSE=True
MOVEMENT_ENABLED=True
LeftTurn = 0.05
RightTurn = 0.05
RobotSpeed = 0.05
NoMarkerTurn = 0.4


class aruco_tracker:

    def __init__(self):

        # Initiate FAST object with default values
        self.fast = cv2.FastFeatureDetector_create(184)

        #This is where we will store the most recent depth array
        self.depth_arr = None

        #This is for how we steeerererererer
        self.xVelocity = 0
        self.zRotation = 0

        #this is where we publish the output
        self.image_pub = rospy.Publisher("/output/image_raw/compressed", CompressedImage, queue_size = 1)
        self.depth_pub = rospy.Publisher("/output/depth/compressed", CompressedImage, queue_size = 1)
        self.velo_pub = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size = 10)

        #this is where we read from the robot
        camera_channel = '/camera/rgb/image_raw/compressed'
        depth_channel = '/camera/depth/image_raw/compressedDepth'
        self.subscriber = rospy.Subscriber(camera_channel,CompressedImage, self.callback, queue_size=1)
        self.depth_subscriber = rospy.Subscriber(depth_channel, CompressedImage, self.depthcallback, queue_size=1)
        if VERBOSE:
            print 'subscribed to ' + camera_channel
            print 'subscribed to ' + depth_channel

    def depthcallback(self, ros_data):
        lengthOfHeader = 12
        raw_data = ros_data.data[lengthOfHeader:]
        np_arr = np.fromstring(raw_data, np.uint8)
        self.depth_arr = cv2.imdecode(np_arr,cv2.IMREAD_ANYDEPTH)
        normalizedImg = None
        normalizedImg = cv2.normalize(self.depth_arr,normalizedImg,0, 255, cv2.NORM_MINMAX,cv2.CV_8UC3)
        histogram = cv2.applyColorMap(normalizedImg,cv2.COLORMAP_RAINBOW)

        if VERBOSE:
            print 'received depth of type: "%s"' % ros_data.format

        # create a compressed image
        msg = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format = 'jpeg'
        msg.data = np.array(cv2.imencode('.jpg', histogram)[1]).tostring()
        # publish that image
        self.depth_pub.publish(msg)

    def callback(self, ros_data):

        #self.xVelocity = 0
        #self.zRotation = 0
        outputText = versionString
        danger = False

        if VERBOSE:
            print 'received image of type: "%s"' % ros_data.format

        np_arr = np.fromstring(ros_data.data, np.uint8)
        image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR) #second argument should be cv2.IMREAD_COLOR for OpenCV >= 3.0

        gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        #red square detection, this should eventually be aruco markers

        #hsv_red = cv2.cvtColor(image_np, cv2.COLOR_BGR2HSV)
        #lower_blue = np.array([0,100,100])
        #upper_blue = np.array([10,255,255])

        #mask = cv2.inRange(hsv_red,lower_blue,upper_blue)

        #n_white_pix = np.sum(mask == 255)

        #aruco marker detection
        aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
        parameters = aruco.DetectorParameters_create()

        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        # find and draw the keypoints
        kp = self.fast.detect(gray)
        danger = False

        for p in kp:
            x,y = p.pt
            x = int(x)
            y = int(y)
            distance = self.depth_arr[y][x]
            if distance > 0:
                if distance < 700: #something is in the danger zone, move away
                    cv2.putText(image_np, (str(distance) + 'mm'), (x, y), font, 1, (255, 0, 255), 2, cv2.LINE_AA)
                    cv2.circle(image_np, (x, y), 1, (0, 0, 255), 5)
                    #TODO add in movement away
                    danger = True
                else:
                    cv2.putText(image_np, (str(distance) + 'mm'), (x, y), font, 1, (0, 0, 180), 2, cv2.LINE_AA)
                    cv2.circle(image_np,(x,y),1,(0,0,255),5)

            if danger:
                self.xVelocity = -0.2
            else:
                self.xVelocity = 0
            # no marker found so continue the turning
            self.zRotation = NoMarkerTurn

        if np.all(ids != None):

            aruco.drawDetectedMarkers(image_np,corners)

            strg = ''
            for i in range(0,ids.size):
                strg += str(ids[i][0])+', '
                #Find the center of the marker
                cX = int((corners[i][0][0][0] + corners[i][0][1][0]) / 2)
                cY = int((corners[i][0][0][1] + corners[i][0][2][1]) / 2)
                distance = self.depth_arr[cY][cX]
                cv2.putText(image_np, (str(distance) + 'mm'), (cX, cY), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
                #TODO get the movement towards
                if not danger:
                    self.xVelocity = 0.2
                    self.zRotation = 0

            height, width = image_np.shape[:2]
            cX = int((corners[0][0][0][0] + corners[0][0][1][0]) / 2)
            outputText += 'spotted: ' + strg

        else:
            outputText += 'No Marker'

        if danger:
            outputText += 'DANGER'
        #Display what was found, marker and its number or no marker
        cv2.putText(image_np, (outputText), (32, 32), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

        #create a compressed image
        msg = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format = 'jpeg'
        msg.data = np.array(cv2.imencode('.jpg',image_np) [1]).tostring()
        #publish that image
        self.image_pub.publish(msg)

        #create a movement message
        move_cmd = Twist()
        if MOVEMENT_ENABLED:
            move_cmd.linear.x = self.xVelocity
            move_cmd.angular.z = self.zRotation
        else:
            move_cmd.linear.x = 0
            move_cmd.angular.z = 0
        self.velo_pub.publish(move_cmd)

def main(args):
    ac = aruco_tracker()
    rospy.init_node('aruco_tracker', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS ArUco Tracker module"
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
