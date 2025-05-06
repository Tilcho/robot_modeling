#!/bin/bash

# Source your ROS workspace
source ~/catkin_ws/devel/setup.bash

# Build the workspace in a new terminal (optional)
gnome-terminal -- bash -c "cd ~/catkin_ws && catkin_make; exec bash"

# Start the ROS launch file in a new terminal
gnome-terminal -- bash -c "cd ~/catkin_ws && source devel/setup.bash && roslaunch painting_cell_moveit demo_gazebo.launch; exec bash"

# Wait for Gazebo to start
sleep 10

# Run hmi_bridge.py in a new terminal
gnome-terminal -- bash -c "cd ~/catkin_ws/src/robot_modeling/painting_cell_moveit/scripts && ./hmi_bridge.py; exec bash"

# Run moveit_hmi.py in a new terminal
gnome-terminal -- bash -c "cd ~/catkin_ws/src/robot_modeling/painting_cell_moveit/scripts && ./moveit_hmi.py; exec bash"
