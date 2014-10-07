cmake_minimum_required(VERSION 2.8.3)
project(velma_description)

find_package(catkin REQUIRED)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES velma_description
#  CATKIN_DEPENDS other_catkin_pkg
#  DEPENDS system_lib
)

install(DIRECTORY urdf robots meshes
 DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)