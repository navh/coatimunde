#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Pose
from math import pow,atan2, sqrt

class GoForward():
    def __init__(self):
        # initiliaze
        rospy.init_node('GoForward', anonymous=False)
	self.pose_subscriber = rospy.Subscriber('/odom', Pose, self.callback)

	# tell user how to stop TurtleBot
	rospy.loginfo("To stop TurtleBot CTRL + C")

        # What function to call when you ctrl + c    
        rospy.on_shutdown(self.shutdown)
        
	# Create a publisher which can "talk" to TurtleBot and tell it to move
        # Tip: You may need to change cmd_vel_mux/input/navi to /cmd_vel if you're not using TurtleBot2
        self.cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
     
	#TurtleBot will stop if we don't keep telling it to move.  How often should we tell it to move? 10 HZ
        r = rospy.Rate(10);

	# as long as you haven't ctrl + c keeping doing...
        while not rospy.is_shutdown():
	    # publish the velocity
            self.cmd_vel.publish(move_cmd)
	    self.userinput()
	    # wait for 0.1 seconds (10 HZ) and publish again
            r.sleep()

    def callback(self, data):
	self.pose = data
	self.pose.x = round(self.pose.x, 4)
	self.pose.y = round(self.pose.y, 4)

    def get_distance(self, goal_x, goal_y):
	distance = sqrt(pow((goal_x - self.pose.x), 2) + pow((goal_y - self.pose.y), 2))
	return distance
	
    def move2goal(self):
	goal_pose = Pose()
	goal_pose.x = input("set the x goal: ")
	goal_pose.y = input("set the y goal: ")
	distance_tolerance = input("set the tolerance: ")
	vel_msg = Twist()

	while sqrt(pow((goal_pose.x - self.pose.x), 2) + pow((goal_pose.y - self.pose.y), 2)) >= distance_tolerance:
		#linear velocity in the x-axis
		vel_msg.linear.x = 1.5*sqrt(pow((goal_pose.x - self.pose.x), 2) + pow((goal_pose.y - self.pose.y),2))
		vel_msg.linear.y = 0
		vel_msg.linear.z = 0

		#angular velocity in z-axiz
		vel_msg.angular.x = 0
		vel_msg.angular.y = 0
		vel_msg.angular.z = 4*(atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x) - self.pose.theta)

		#publishing the vel_msg
		self.velocity_publisher.publish(vel_msg)
		self.rate.sleep()
	#stopping the robot at the end
	vel_msg.linear.x = 0
	vel_msg.angular.z = 0
	self.velocity_publisher.publish(vel_msg)
	rospy.spin()
	        
    def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stop TurtleBot")
	# a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
        self.cmd_vel.publish(Twist())
	# sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
        rospy.sleep(1)
 
if __name__ == '__main__':
    try:
        GoForward()
    except:
        rospy.loginfo("GoForward node terminated.")


