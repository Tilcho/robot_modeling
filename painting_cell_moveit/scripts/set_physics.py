#!/usr/bin/env python3
import rospy
from gazebo_msgs.srv import SetPhysicsProperties
from gazebo_msgs.msg import ODEPhysics
from geometry_msgs.msg import Vector3

def set_physics():
    rospy.init_node('set_gazebo_physics')
    rospy.wait_for_service('/gazebo/set_physics_properties')
    try:
        set_physics = rospy.ServiceProxy('/gazebo/set_physics_properties', SetPhysicsProperties)
        set_physics(
            time_step=0.005,
            max_update_rate=5000.0,
            gravity=Vector3(0, 0, -9.81),
            ode_config=ODEPhysics()
        )
        rospy.loginfo("Gazebo physics properties updated.")
    except rospy.ServiceException as e:
        rospy.logerr("Service call failed: %s" % e)

if __name__ == "__main__":
    set_physics()
