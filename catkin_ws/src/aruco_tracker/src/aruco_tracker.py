#! /usr/bin/env python


#python libs
import sys, time

#numpy and scipy
import numpy as np
from scipy.ndimage import filters

#openCV
import cv2

#ros libraries
import roslib
import rospy

#ros messages
from sensor_msgs.msg import CompressedImage

VERBOSE=True

class image_feature:

    def __init__(self):
        #this is where we publish the output
        self.image_pub = rospy.Publisher("/output/image_raw/compressed", CompressedImage)

        #this is where we read from the robot
        self.subscriber = rospy.Subscriber("/camera/rgb/image_raw/compressed",CompressedImage, self.callback, queue_size=1)
        if VERBOSE:
            print "subscribed to /camera/image/compressed"

    def callback(self, ros_data):
        if VERBOSE:
            print 'received image of type: "%s"' % ros_data.format

        np_arr = np.fromstring(ros_data.data, np.uint8)
        image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR) #second argument should be cv2.IMREAD_COLOR for OpenCV >= 3.0

        method = "GridFAST"
        feat_det = cv2.FeatureDetector_create(method)
        time1 = time.time()

        featPoints = feat_det.detect(cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY))
        time2 = time.time()

        if VERBOSE:
            print "%s detector found: %s points in: %s sec."%(method,len(featPoints),(time2-time1))

        for point in featPoints:
            x,y = point.pt
            cv2.circle(image_np,(int(x),int(y)), 3, (0,0,255), -1)

        #create a compressed image
        msg = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format = 'jpeg'
        msg.data = np.array(cv2.imencode('.jpg',image_np) [1]).tostring()
        #publish that image
        self.image_pub.publish(msg)

def main(args):
    ic = image_feature()
    rospy.init_node('image_feature', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS ArUco Tracker module"
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
