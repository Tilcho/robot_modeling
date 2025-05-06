cmake_minimum_required(VERSION 3.1.3)
project(painting_cell_moveit)

find_package(catkin REQUIRED)

catkin_package()

install(DIRECTORY launch DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
  PATTERN "setup_assistant.launch" EXCLUDE)
install(DIRECTORY config DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

catkin_install_python(PROGRAMS
  scripts/hmi_bridge.py
  scripts/moveit_hmi.py
  scripts/paint.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)