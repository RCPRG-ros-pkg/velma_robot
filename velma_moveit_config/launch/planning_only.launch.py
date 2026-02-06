#!/usr/bin/env python3
import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration, Command, FindExecutable
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

from moveit_configs_utils import MoveItConfigsBuilder


def _launch_setup(context, *args, **kwargs):
    config_pkg = LaunchConfiguration("config_pkg").perform(context)
    robot_name = LaunchConfiguration("robot_name").perform(context)

    urdf_file = LaunchConfiguration("urdf_file").perform(context)   # np. urdf/robot.urdf.xacro
    srdf_file = LaunchConfiguration("srdf_file").perform(context)   # np. srdf/robot.srdf
    rviz_file = LaunchConfiguration("rviz_config").perform(context) # np. rviz/moveit.rviz

    use_joint_state_gui = LaunchConfiguration("use_joint_state_gui").perform(context).lower() in ("true", "1", "yes")
    world_frame = LaunchConfiguration("world_frame").perform(context)
    base_frame = LaunchConfiguration("base_frame").perform(context)

    pkg_share = get_package_share_directory(config_pkg)
    urdf_path = os.path.join(pkg_share, urdf_file)
    srdf_path = os.path.join(pkg_share, srdf_file)
    rviz_path = os.path.join(pkg_share, rviz_file)

    robot_description = {
        "robot_description": ParameterValue(
            Command([FindExecutable(name="xacro"), " ", urdf_path]),
            value_type=str,
        )
    }

    with open(srdf_path, "r", encoding="utf-8") as f:
        robot_description_semantic = {"robot_description_semantic": f.read()}

    moveit_config = (
        MoveItConfigsBuilder(robot_name, package_name=config_pkg)
        .robot_description(file_path=urdf_path)
        .robot_description_semantic(file_path=srdf_path)
        .robot_description_kinematics(file_path="config/kinematics.yaml")
        .joint_limits(file_path="config/joint_limits.yaml")
        .planning_pipelines(pipelines=["ompl"])
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .planning_scene_monitor(publish_robot_description=True, publish_robot_description_semantic=True)
        .to_moveit_configs()
    )

    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            moveit_config.to_dict(),
            robot_description,
            robot_description_semantic,
            {"allow_trajectory_execution": False},
        ],
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        output="log",
        arguments=["-d", rviz_path],
        parameters=[
            robot_description,
            robot_description_semantic,
            moveit_config.robot_description_kinematics,
            moveit_config.planning_pipelines,
            moveit_config.joint_limits,
        ],
    )

    rosbridge_websocket_node = Node(
        package="rosbridge_server",
        executable="rosbridge_websocket",
        output="log",
        #arguments=["-d", rviz_path],
        parameters=[
            {"delay_between_messages": 0.0},
        ],
    )
    # ros2 run rosbridge_server rosbridge_websocket --ros-args -p delay_between_messages:=0.0

    joint_state_node = Node(
        package="joint_state_publisher_gui" if use_joint_state_gui else "joint_state_publisher",
        executable="joint_state_publisher_gui" if use_joint_state_gui else "joint_state_publisher",
        output="log",
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[robot_description],
    )

    static_tf = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        output="log",
        arguments=["--frame-id", world_frame, "--child-frame-id", base_frame],
    )

    return [
        # joint_state_node,
        # robot_state_publisher_node,
        # static_tf,
        move_group_node,
        rviz_node,
        rosbridge_websocket_node,
    ]


def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument("config_pkg", default_value="velma_moveit_config"),
            DeclareLaunchArgument("robot_name", default_value="velma"),
            DeclareLaunchArgument("urdf_file", default_value="config/velma.urdf.xacro"),
            DeclareLaunchArgument("srdf_file", default_value="config/velma.srdf"),
            DeclareLaunchArgument("rviz_config", default_value="config/moveit.rviz"),
            DeclareLaunchArgument("use_joint_state_gui", default_value="true"),
            DeclareLaunchArgument("world_frame", default_value="world"),
            DeclareLaunchArgument("base_frame", default_value="base_link"),
            OpaqueFunction(function=_launch_setup),
        ]
    )
