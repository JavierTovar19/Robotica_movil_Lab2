#!/usr/bin/env python3.8

import rospy 
from geometry_msgs.msg import Twist 
from random import random 
from turtlesim.msg import Pose 
import numpy as np

class bot:
    def __init__(self, rate=10):
        rospy.init_node('pypubvel', anonymous=False) 
        self.pose = rospy.Subscriber("/turtle1/pose", Pose, self.callback_pose)
        self.pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
        self.x = 0
        self.y=0
        self.yaw=0
        self.rate=rospy.Rate(rate)
        self.distancia=0
        self.angulo=0
        self.tolerancia=0.01
        self.kp_dist = 1.0
        self.kp_ang = 1.0

    def callback_pose(self,msg):
        self.x = msg.x
        self.y = msg.y
        self.yaw = msg.theta

    def move(self,linear,angular):
        msg = Twist()
        msg.linear.x = linear
        msg.angular.z = angular
        self.pub.publish(msg)

    def goto(self, x_o, y_o, dx, dt):
        self.distancia = np.sqrt((x_o - self.x)**2 + (y_o - self.y)**2)
        angulo_objetivo = np.arctan2(y_o - self.y, x_o - self.x)
        error_ang = np.arctan2(np.sin(angulo_objetivo - self.yaw),
                            np.cos(angulo_objetivo - self.yaw))
        
        if np.abs(error_ang) < self.tolerancia and self.distancia < self.tolerancia:
            self.move(0, 0)
            return True
        vel_lineal = self.kp_dist * self.distancia
        if np.abs(error_ang) > self.tolerancia:
            vel_lineal = 0  
        vel_lineal=np.clip(vel_lineal,0,dx)
        vel_angular = self.kp_ang * error_ang
        vel_angular = np.clip(vel_angular, -dt,dt)
        
        self.move(vel_lineal, vel_angular)
        return False


if __name__ == '__main__': 
    try:
        objetivos=[[5,5],[7,5],[7.5,7],[6,8],[4.5,7]]
        obj_act=objetivos[0]
        turtle = bot()
        turtle.tolerancia=0.1
        turtle.rate= rospy.Rate(10)
        max_vel_lin=1
        max_vel_w=1
        while not rospy.is_shutdown():
            rospy.loginfo(f'Giro:\n x= {turtle.x}\n y= {turtle.y}\n yaw= {turtle.yaw}')
            if turtle.goto(obj_act[0],obj_act[1], max_vel_lin,max_vel_w):
                objetivos.pop(0)
                objetivos.append(obj_act)
                obj_act=objetivos[0]

            rospy.loginfo(f'Giro:\n angulo_actual= {turtle.yaw}\n angulo_deseado= {turtle.angulo}, diferencia= {np.abs(turtle.angulo-turtle.yaw)}')
            turtle.rate.sleep()
    except rospy.ROSInterruptException:
        pass