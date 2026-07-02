import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg_path = get_package_share_directory('arm_4dof')
    arm_urdf = os.path.join(pkg_path,'urdf','arm.urdf')
    rviz_file = os.path.join(pkg_path,'rviz','arm.rviz')

    with open(arm_urdf,'r') as urdf:
        robot_desc = urdf.read()

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_desc}]
        ),

        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            arguments=['-d', rviz_file]
        ),

        #Node(
        #    package="joint_state_publisher_gui",
        #    executable="joint_state_publisher_gui"
        #)
    ])
