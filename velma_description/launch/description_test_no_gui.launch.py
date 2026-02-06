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
            package="rviz2",
            executable="rviz2",
            output="screen",
            arguments=[
                "-d", rviz_config_path,
                #"--ros-args", "--log-level", "debug",
            ],
        ),
    ])
