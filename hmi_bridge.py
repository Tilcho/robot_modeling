#!/usr/bin/env python
import rospy
from std_msgs.msg import String, Float64MultiArray
from moveit_commander import MoveGroupCommander, roscpp_initialize, roscpp_shutdown
from geometry_msgs.msg import Pose

def handle_joystick_command(msg):
    try:
        parts = msg.data.split(":")
        robot_name = parts[0]
        target_type = parts[1]  # "joint" oder "tcp"
        move_target = parts[2]  # z. B. "joint_1" oder "x"
        direction = parts[3]    # "up"/"down"

        delta = 0.05 if direction == "up" else -0.05
        group = move_groups.get(robot_name)
        if not group:
            rospy.logwarn("Unbekannter Roboter: %s" % robot_name)
            return

        if target_type == "joint":
            joint_map = {
                "joint_1": 0, "joint_2": 1, "joint_3": 2,
                "joint_4": 3, "joint_5": 4, "joint_6": 5
            }
            if move_target not in joint_map:
                rospy.logwarn("Ungültiger Joint: %s" % move_target)
                return
            idx = joint_map[move_target]
            joint_values = group.get_current_joint_values()
            joint_values[idx] += delta
            group.go(joint_values, wait=True)

        elif target_type == "tcp":
            pose = group.get_current_pose().pose
            if move_target == "x":
                pose.position.x += delta
            elif move_target == "y":
                pose.position.y += delta
            elif move_target == "z":
                pose.position.z += delta
            else:
                rospy.logwarn("Ungültige TCP-Achse")
                return
            group.set_pose_target(pose)
            group.go(wait=True)

    except Exception as e:
        rospy.logerr(f"Joystick-Fehler: {e}")

def publish_status(event):
    for name, group in move_groups.items():
        joint_vals = group.get_current_joint_values()
        pub = status_publishers[name]
        msg = Float64MultiArray(data=joint_vals)
        pub.publish(msg)

if __name__ == "__main__":
    import sys
    roscpp_initialize(sys.argv)
    rospy.init_node("hmi_bridge", anonymous=True)

    move_groups = {
        "lackierer": MoveGroupCommander("move_group_1"),
        "uv": MoveGroupCommander("move_group_2")
    }
    for g in move_groups.values():
        g.set_max_velocity_scaling_factor(0.1)

    rospy.Subscriber("joystick_cmd", String, handle_joystick_command)

    # Status-Topics publizieren
    status_publishers = {
        "lackierer": rospy.Publisher("status_lackierer", Float64MultiArray, queue_size=10),
        "uv": rospy.Publisher("status_uv", Float64MultiArray, queue_size=10)
    }

    rospy.Timer(rospy.Duration(1.0), publish_status)
    rospy.loginfo("HMI-Bridge läuft...")
    rospy.spin()
    roscpp_shutdown()

