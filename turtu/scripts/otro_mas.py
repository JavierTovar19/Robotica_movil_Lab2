#!/usr/bin/env python3.8


import rospy 
from geometry_msgs.msg import Twist 
from random import random 
from turtlesim.msg import Pose 
import numpy as np

radio_muro=1
limites=[0,11]
velocidad_l=5
velocidad_w=7
frec=30

X=0
Y=0
Z=0

def callback(data):
    global X
    global Y
    global Z
    X = data.x
    Y = data.y
    Z = data.theta

def sentido(X,Y,Z):
    if X>limites[1]-radio_muro:
        if Z>0:
            return velocidad_w
        else:
            return -velocidad_w
    elif X<limites[0]+radio_muro:
        if Z<np.pi and Z>0:
            return -velocidad_w
        else:
            return velocidad_w
    elif Y>limites[1]-radio_muro:
        if Z<np.pi/2:
            return -velocidad_w
        else:
            return velocidad_w
    elif Y<limites[0]+radio_muro:
        if Z>-np.pi/2:
            return velocidad_w
        else:
            return -velocidad_w
        


if __name__ == '__main__': 
    try:
    # Create a publisher on topic turtle1/cmd_vel, type geometry_msgs/Twist
        pub = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=1000) 
        rospy.init_node('pypubvel', anonymous=False) 
        sub = rospy.Subscriber('turtle1/pose', Pose, callback)
        rate = rospy.Rate(2) 
        rate = rospy.Rate(frec)
        # Similar to while(ros::ok()) 
        while not rospy.is_shutdown():
            
        # Create and populate new Twist message 
            if(X>limites[1]-radio_muro or X<limites[0]+radio_muro or Y>limites[1]-radio_muro or Y<limites[0]+radio_muro):
                vw= sentido(X,Y,Z)
                msg = Twist()
                msg.linear.x = velocidad_l
                msg.angular.z =vw
                rospy.loginfo(f'Giro:\n linear= {msg.linear.x}\n angular= {msg.angular.z}')
                rate.sleep() 
            else: 
                msg = Twist()
                msg.linear.x = velocidad_l
                msg.angular.z =0 
                rospy.loginfo(f'Avance:\n linear= {msg.linear.x}\n angular= {msg.angular.z}')
                rate.sleep() 

            # Similar to ROS_INFO_STREAM macro, log information.

            # Publish the message and wait on rate.
            pub.publish(msg)
            rate.sleep()
    except rospy.ROSInterruptException:
        pass