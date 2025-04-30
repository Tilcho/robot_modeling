#!/usr/bin/env python3
import copy
import rospy
import roslaunch
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import numpy as np
import sys
import math
import time 

class demo_robot:
    def __init__(self,nodename="demo_robot",groupname="robot_flo"):
        rospy.init_node(nodename, anonymous=False)
        moveit_commander.roscpp_initialize(sys.argv)
        self.robot = moveit_commander.RobotCommander()
        self.move_group = moveit_commander.MoveGroupCommander(groupname)
        
        #Acceleration and Speed factors
        self.move_group.set_max_acceleration_scaling_factor(1)
        self.move_group.set_max_velocity_scaling_factor(1)
        
        self.move_group.set_goal_tolerance(0.001) #For real robot set the tolerance to 1 mm
        self.goals = []

    def getPoseAndPrint(self):
        self.cp = self.move_group.get_current_pose().pose
        print("Info: current pose ")
        print("x: ",self.cp.position.x)
        print("y: ",self.cp.position.y)
        print("z: ",self.cp.position.z)
        print("qx: ",self.cp.orientation.x)
        print("qy: ",self.cp.orientation.y)
        print("qz: ",self.cp.orientation.z)
        print("qw: ",self.cp.orientation.w)

    def setTarget(self,x,y,z,roll,pitch,yaw):
        goal = geometry_msgs.msg.Pose()

        qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
        qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
        qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
        qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

        goal.position.x = x
        goal.position.y = y
        goal.position.z = z
        goal.orientation.x = qx
        goal.orientation.y = qy
        goal.orientation.z = qz
        goal.orientation.w = qw

        try:
            self.goals.append(copy.deepcopy(goal))
    
        except:
            print("Target not set")

    def move(self):

        self.move_group.clear_pose_targets()
        try:
            for g in self.goals:
                self.move_group.set_pose_target(g)
                self.move_group.go(wait=True)
        except:
            print("Targets not reachable")
        finally:
            print("Stopping")
            self.move_group.stop()
            self.move_group.clear_pose_targets()
            self.goals = []

if __name__ == "__main__":
    r = demo_robot(nodename="demo_robot",groupname="robot_flo")
    
    r.setTarget(0.25,0,0.30,    3.14,0,0)
    r.setTarget(0.25,0.2,0.30,  3.14,0,0)
    r.setTarget(0.25,0.2,0.1,   3.14,0,0)
    r.setTarget(0.25,0.2,0.30,  3.14,0,0)
    r.setTarget(0.25,-0.2,0.30, 3.14,0,0)
    r.setTarget(0.25,-0.2,0.1,  3.14,0,0)
    r.setTarget(0.25,-0.2,0.30, 3.14,0,0)
    r.setTarget(0.25,0,0.30,    3.14,0,0)
    r.move()
    
    del r
