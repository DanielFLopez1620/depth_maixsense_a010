#!/usr/bin/env python3
#
# Quick standalone test launch.
#
# Spawns a fake TF tree (base_link -> camera_link -> camera_link_optical) so the
# camera can be visualized as if mounted on a robot, WITHOUT needing the real
# robot running. The two static transforms produce the three frames:
#   base_link --(mounting offset)--> camera_link --(optical rotation)--> camera_link_optical
#
# For integration with the real robot, use maixsense_a010_launch.py instead and
# let the robot publish base_link / camera_link.

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    package_name = 'depth_maixsense_a010'
    # This test relies on base_link existing, so it uses the base_link config.
    rviz_config_path = os.path.join(get_package_share_directory(package_name), 'rviz', 'maix.rviz')

    return LaunchDescription([
        DeclareLaunchArgument(
            'rviz_config',
            default_value=rviz_config_path,
            description='Ruta al archivo de configuración de RViz'
        ),

        DeclareLaunchArgument(
            'device',
            default_value='/dev/ttyUSB0',
            description='Puerto serial de la cámara MaixSense A010'
        ),

        # base_link -> camera_link : mounting offset of the camera on the robot.
        # Adjust x/y/z (meters) to match where the camera actually sits.
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='tf_base_to_camera_link',
            output='screen',
            arguments=[
                '--x', '0.10', '--y', '0.0', '--z', '0.20',
                '--roll', '0.0', '--pitch', '0.0', '--yaw', '0.0',
                '--frame-id', 'base_link',
                '--child-frame-id', 'camera_link',
            ]
        ),

        # camera_link -> camera_link_optical : REP-103 optical rotation
        # (body frame x-forward/z-up  ->  optical frame z-forward/x-right/y-down).
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='tf_camera_link_to_optical',
            output='screen',
            arguments=[
                '--x', '0.0', '--y', '0.0', '--z', '0.0',
                '--roll', '-1.5708', '--pitch', '0.0', '--yaw', '-1.5708',
                '--frame-id', 'camera_link',
                '--child-frame-id', 'camera_link_optical',
            ]
        ),

        Node(
            package=package_name,
            executable='publisher',
            name='depth_maixsense_a010_publisher',
            output='screen',
            parameters=[{'device': LaunchConfiguration('device')}]
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', LaunchConfiguration('rviz_config')]
        )
    ])
