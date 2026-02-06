from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, FindExecutable
from ament_index_python.packages import get_package_share_directory
from launch_ros.parameter_descriptions import ParameterValue
import os

def generate_launch_description():
    share = get_package_share_directory("velma_description")
    xacro_path = os.path.join(share, "urdf", "velma.urdf.xacro")

    rviz_config_path = os.path.join(share, "rviz", "velma.rviz")

    # TODO: fill parameters for xacro
    robot_description = {
        "robot_description": ParameterValue(
            Command([FindExecutable(name="xacro"),
            " ", xacro_path,
            #" ", "use_sim:=false",
            " ", "mobile_base:=false",
            " ", "use_gazebo_kinect:=true",
            " ", "use_stereo_pair:=true",
            " ", "use_left_optoforces:=false",
            " ", "use_right_optoforces:=false",
            " ", "use_gpu:=true",
            " ", "use_dh_compatible_model:=false",
            " ", "collision_detector:=fcl"
            ]),
            value_type=str,
        )
    }

    return LaunchDescription([
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[robot_description],
            output="screen",
        ),
        Node(
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui",
            output="screen",
        ),
        Node(
            package="rviz2",
            executable="rviz2",
            output="screen",
            arguments=[
                "-d", rviz_config_path,
                #"--ros-args", "--log-level", "debug",
            ],
        ),
    ])





  # <arg name="load_velma_sim_gazebo" default="false"/>
  # <arg name="use_dh_compatible_model" default="false"/>
  # <arg name="use_left_optoforces" default="false"/>
  # <arg name="use_right_optoforces" default="false"/>
  # <arg name="mobile_base" default="false"/>
  # <arg name="use_gpu_ray" default="true"/>
  # <arg name="collision_detector" default="fcl"/>
  # <arg name="use_kinect" default="true"/>
  # <arg name="use_stereo_pair" default="true"/>

  # <arg unless="$(arg load_velma_sim_gazebo)" name="__cmd_velma_sim_gazebo" value="subsystem_xml:=false"/>
  # <arg     if="$(arg load_velma_sim_gazebo)" name="__cmd_velma_sim_gazebo" value="xml_file_re_body:='$(find velma_sim_gazebo)/config/velma_core_re.xml' subsystem_xml:=true"/>

  # <arg unless="$(arg mobile_base)" name="__srdf_filename" value="velma.srdf"/>
  # <arg     if="$(arg mobile_base)" name="__srdf_filename" value="velma_mobile.srdf"/>

  # <param
  #   name="/robot_description"
  #   command="$(find xacro)/xacro
  #     '$(find velma_description)/robots/velma.urdf.xacro'
  #     $(arg __cmd_velma_sim_gazebo)
  #     mobile_base:=$(arg mobile_base)
  #     use_gazebo_kinect:=$(arg use_kinect)
  #     use_stereo_pair:=$(arg use_stereo_pair)
  #     use_left_optoforces:=$(arg use_left_optoforces)
  #     use_right_optoforces:=$(arg use_right_optoforces)
  #     use_gpu:=$(arg use_gpu_ray)
  #     use_dh_compatible_model:=$(arg use_dh_compatible_model)
  #     collision_detector:=$(arg collision_detector)"
  #     