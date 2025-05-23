#!/usr/bin/env python3
import rospy
import moveit_commander
import sys
import math

class MultiRobotDemo:
    def __init__(self):
        rospy.init_node("multi_robot_demo", anonymous=False)
        moveit_commander.roscpp_initialize(sys.argv)

        # Initialize MoveGroups for all manipulators
        self.robot_simon = moveit_commander.MoveGroupCommander("robot_simon")
        self.robot_flo = moveit_commander.MoveGroupCommander("robot_flo")
        self.turn_table = moveit_commander.MoveGroupCommander("turn_table")
        self.move_group = moveit_commander.MoveGroupCommander("robot_simon")
        self.move_group.set_goal_tolerance(0.1)

        for group in [self.robot_simon, self.robot_flo, self.turn_table]:
            group.set_max_acceleration_scaling_factor(1.0)
            group.set_max_velocity_scaling_factor(1.0)
            group.set_goal_tolerance(0.001)

    def move_named_target(self, group, target_name, wait_for_it):
        rospy.loginfo(f"Moving {group.get_name()} to {target_name}")
        group.set_start_state_to_current_state()
        group.set_named_target(target_name)
        success = group.go(wait=wait_for_it)
        group.stop()
        group.clear_pose_targets()
        rospy.sleep(1.0)

        if not success:
            rospy.logwarn(f"Failed to reach target: {target_name}")

    def run_sequence(self):
        doSimon = True
        # All robots to home position before any operation
        self.move_named_target(self.turn_table, "home", False)
        self.move_named_target(self.robot_simon, "home", False)
        self.move_named_target(self.robot_flo, "home", False)

        # Turntable to station_1
        self.move_named_target(self.turn_table, "station_1", True)

        # robot_simon executes paint sequence
        for i in range(1, 10):
            self.move_named_target(self.robot_simon, f"paint_{i}", True)
        self.move_named_target(self.robot_simon, "home", True)

        # Turntable to station_2
        self.move_named_target(self.turn_table, "station_2", True)

        # robot_flo executes cure sequence
        for i in range(1, 5):
            self.move_named_target(self.robot_flo, f"cure_{i}", True)
        self.move_named_target(self.robot_flo, "home", True)

        # Turntable to station_3
        self.move_named_target(self.turn_table, "home", False)

        rospy.loginfo("Process completed.")

if __name__ == "__main__":
    demo = MultiRobotDemo()
    demo.run_sequence()
