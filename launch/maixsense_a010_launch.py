#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    package_name = 'depth_maixsense_a010'
    # Camera-only launch (no TF tree): use the optical config whose Fixed Frame
    # is camera_link_optical, so the cloud renders even without any robot TF.
    rviz_config_path = os.path.join(get_package_share_directory(package_name), 'rviz', 'maix_optical.rviz')
    
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
