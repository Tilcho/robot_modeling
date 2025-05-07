#!/bin/bash

# Go to your workspace
cd ~/catkin_ws

# Source your ROS workspace
source devel/setup.bash

# Build your ROS workspace
catkin_make

# Start the ROS launch file in a new terminal
gnome-terminal -- bash -c "cd ~/catkin_ws && source devel/setup.bash && roslaunch painting_cell_moveit demo_gazebo.launch; exec bash"

# Wait for Gazebo to start
sleep 30

# Run hmi_bridge.py in a new terminal
gnome-terminal -- bash -c "cd ~/catkin_ws/src/robot_modeling/painting_cell_moveit/scripts && ./hmi_bridge.py; exec bash"

# Wait for Bridge to Connect
sleep 15

# Run moveit_hmi.py in a new terminal
gnome-terminal -- bash -c "cd ~/catkin_ws/src/robot_modeling/painting_cell_moveit/scripts && ./moveit_hmi.py; exec bash"
