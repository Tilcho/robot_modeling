#!/usr/bin/env python3

import rospy
import moveit_commander
import numpy as np
import sys
import math
import time

def main():
    # Initialize ROS and MoveIt
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('simple_joint_mover_dual', anonymous=True)

    # Create RobotCommander and two MoveGroupCommanders
    robot = moveit_commander.RobotCommander()
    group_flo = moveit_commander.MoveGroupCommander("robot_flo")
    group_simon = moveit_commander.MoveGroupCommander("robot_simon")

    # Allow replanning if plan fails
    group_flo.allow_replanning(True)
    group_simon.allow_replanning(True)

    # Print active joints for each robot
    print("robot_flo joints: ", group_flo.get_active_joints())
    print("robot_simon joints: ", group_simon.get_active_joints())

    # Move robot_flo joint_1 and robot_simon joint_2
    # ------------------------------------------------
    
    ## FLO: Move joint_1 (index 0)
    flo_goal = group_flo.get_current_joint_values()
    
    ## SIMON: Move joint_2 (index 1)
    simon_goal = group_simon.get_current_joint_values()

    ampl = math.pi/2

    # Step 1: -pi
    flo_goal[0] = -ampl
    simon_goal[1] = -ampl
    group_flo.go(flo_goal, wait=True)
    group_simon.go(simon_goal, wait=True)  # Wait only for simon to finish
    group_flo.stop()
    group_simon.stop()
    rospy.sleep(1.0)

    # Step 2: +pi
    flo_goal[0] = ampl
    simon_goal[1] = ampl
    group_flo.go(flo_goal, wait=True)
    group_simon.go(simon_goal, wait=True)
    group_flo.stop()
    group_simon.stop()
    rospy.sleep(1.0)

    # Step 3: back to 0
    flo_goal[0] = 0.0
    simon_goal[1] = 0.0
    group_flo.go(flo_goal, wait=True)
    group_simon.go(simon_goal, wait=True)
    group_flo.stop()
    group_simon.stop()

    print("Motion finished.")

if __name__ == '__main__':
    main()
