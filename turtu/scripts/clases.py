#!/usr/bin/env python3.8

import rospy 
from geometry_msgs.msg import Twist 
from random import random 
from turtlesim.msg import Pose 
import numpy as np
from std_srvs.srv import Empty

class bot:
    def __init__(self, rate=10):
        rospy.init_node('control', anonymous=False) 
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
        self.clear_srv = rospy.ServiceProxy('/clear', Empty)

    def callback_pose(self,msg):
        self.x = msg.x
        self.y = msg.y
        self.yaw = msg.theta

    def move(self,linear,angular):
        msg = Twist()
        msg.linear.x = linear
        msg.angular.z = angular
        self.pub.publish(msg)

    def sentido(self, X, Y, Z, velocidad_w):

        min_lim, max_lim = limites[0], limites[1]
        radio = radio_muro
        
        cerca_muro = False
        dir_deseada_x = 0.0
        dir_deseada_y = 0.0
        
        if X > max_lim - radio:          # Muro derecho
            cerca_muro = True
            dir_deseada_x -= 1.0
        if X < min_lim + radio:          # Muro izquierdo
            cerca_muro = True
            dir_deseada_x += 1.0
        if Y > max_lim - radio:          # Muro superior
            cerca_muro = True
            dir_deseada_y -= 1.0
        if Y < min_lim + radio:          # Muro inferior
            cerca_muro = True
            dir_deseada_y += 1.0
        
        if not cerca_muro:
            return 0.0 

        if dir_deseada_x != 0 or dir_deseada_y != 0:
            angulo_objetivo = np.arctan2(dir_deseada_y, dir_deseada_x)
        else:
            angulo_objetivo = Z
        
        error = np.arctan2(np.sin(angulo_objetivo - Z), np.cos(angulo_objetivo - Z))
        
        if np.abs(error) > 0.01:
            if error > 0:
                return velocidad_w 
            else:
                return -velocidad_w
        else:
            return 0.0
    
    def change_background(self, r, g, b):
        rospy.set_param('/turtlesim/background_r', r)
        rospy.set_param('/turtlesim/background_g', g)
        rospy.set_param('/turtlesim/background_b', b)
        self.clear_srv()
        rospy.loginfo(f"Color de fondo cambiado a: R={r}, G={g}, B={b}")
        

if __name__ == '__main__': 
    try:
        turtle = bot()
        turtle.rate= rospy.Rate(60)
        turtle.change_background(255,0,0)
        max_vel_x=6
        max_vel_w=12
        limites=[0,11]
        radio_muro=1

        while not rospy.is_shutdown():
            vw= turtle.sentido(turtle.x,turtle.y,turtle.yaw, max_vel_w)
            turtle.move(max_vel_x,vw)
            rospy.loginfo(f'Giro:\n linear= {max_vel_x}\n angular= {vw}')
            turtle.rate.sleep()

    except rospy.ROSInterruptException:
        pass
