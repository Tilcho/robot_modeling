#!/usr/bin/env python3

import rospy
import moveit_commander
import sys

def move_to_named_target(group, target_name):
    rospy.loginfo(f"Moving to: {target_name}")

    # Always update start state to current robot state
    group.set_start_state_to_current_state()

    group.set_named_target(target_name)
    success = group.go(wait=True)
    group.stop()
    group.clear_pose_targets()
    rospy.sleep(1.0)
    return success

def main():
    # Initialize MoveIt and ROS
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('named_target_sequence', anonymous=True)

    # Create interfaces
    robot = moveit_commander.RobotCommander()
    group = moveit_commander.MoveGroupCommander("robot_simon")

    # Allow replanning
    group.allow_replanning(True)

    # Print joint names for verification
    print("Controlling joints: ", group.get_active_joints())

    # Define the sequence of named targets
    named_targets = ["home", "paint_1", "paint_2", "paint_3", "paint_4", "home"]

    # Move through each target
    for target in named_targets:
        success = move_to_named_target(group, target)
        if not success:
            rospy.logwarn(f"Failed to reach target: {target}")
            break

    rospy.loginfo("Motion sequence finished.")

if __name__ == '__main__':
    main()
