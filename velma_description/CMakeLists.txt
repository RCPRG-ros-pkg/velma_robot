cmake_minimum_required(VERSION 3.16)
project(velma_description)

find_package(ament_cmake REQUIRED)

install(DIRECTORY rviz urdf meshes materials calibration launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()