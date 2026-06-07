from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

from moveit_configs_utils import MoveItConfigsBuilder
from ament_index_python.packages import get_package_share_directory
import os
import yaml

def load_yaml(package_name, file_path):
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, file_path)
    with open(absolute_file_path, "r") as f:
        return yaml.safe_load(f)

def generate_launch_description():
    use_sim_time = LaunchConfiguration("use_sim_time")

    moveit_config = (
        MoveItConfigsBuilder("velma", package_name="velma_moveit_config")
        .trajectory_execution(
            file_path="config/moveit_controllers.yaml",
            moveit_manage_controllers=False,
        )
        .planning_scene_monitor(
            publish_planning_scene=True,
            publish_geometry_updates=True,
            publish_state_updates=True,
            publish_transforms_updates=True,
            publish_robot_description=True,
            publish_robot_description_semantic=True,
        )
        .to_moveit_configs()
    )

    move_group_configuration = {
        "use_sim_time": use_sim_time,
        "allow_trajectory_execution": True,
        "publish_robot_description_semantic": True,
        "publish_planning_scene": True,
        "publish_geometry_updates": True,
        "publish_state_updates": True,
        "publish_transforms_updates": True,
        "monitor_dynamics": False,

        # Zostawione jak w standardowym generate_move_group_launch:
        # "capabilities": ParameterValue("", value_type=str),
        "disable_capabilities": ParameterValue("", value_type=str),
        "capabilities": "move_group/ExecuteTaskSolutionCapability",
    }

    robot_ns = LaunchConfiguration("robot_ns")

    sensors_3d = load_yaml("velma_moveit_config", "config/sensors_3d.yaml")
    octomap_config = {
        "octomap_frame": "world",
        "octomap_resolution": 0.05,
        "max_range": 5.0,
    }

    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        namespace=robot_ns,
        output="screen",
        parameters=[
            moveit_config.to_dict(),
            move_group_configuration,
            sensors_3d,
            octomap_config,
        ],
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            "use_sim_time",
            default_value="true",
            description="Use simulation clock",
        ),
        DeclareLaunchArgument(
                "robot_ns",
                default_value="",
                description="Robot namespace",
            ),
        move_group_node,
    ])
