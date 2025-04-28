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
    rospy.init_node('simple_joint_mover', anonymous=True)

    # Create RobotCommander and MoveGroupCommander for robot_flo
    robot = moveit_commander.RobotCommander()
    group = moveit_commander.MoveGroupCommander("robot_flo")

    # Allow replanning if plan fails
    group.allow_replanning(True)

    # Print joint names (for confirmation)
    print("Controlling joints: ", group.get_active_joints())

    # Get current joint values
    joint_goal = group.get_current_joint_values()

    # Move joint_1_flo (index 0) to -pi
    joint_goal[0] = -math.pi/2
    group.go(joint_goal, wait=True)
    group.stop()

    rospy.sleep(1.0)

    # Move joint_1_flo (index 0) to +pi
    joint_goal[0] = math.pi/2
    group.go(joint_goal, wait=True)
    group.stop()

    rospy.sleep(1.0)

    # Move joint_1_flo (index 0) back to 0
    joint_goal[0] = 0.0
    group.go(joint_goal, wait=True)
    group.stop()

    print("Motion finished.")

if __name__ == '__main__':
    main()
