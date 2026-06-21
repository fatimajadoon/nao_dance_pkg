# nao_dance.launch.py
# Author: Fatima Jadoon
# Launches Webots with the NAO dance stadium world.

import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess


def generate_launch_description():
    from ament_index_python.packages import get_package_share_directory
    package_dir = get_package_share_directory('nao_dance_pkg')
    world_file  = os.path.join(package_dir, 'worlds', 'nao_dance_stadium.wbt')

    webots = ExecuteProcess(
        cmd=['/usr/local/webots/webots', world_file],
        additional_env={'WEBOTS_HOME': '/usr/local/webots'},
        output='screen'
    )

    return LaunchDescription([webots])
