from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import LifecycleNode, Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
import os

def generate_launch_description():
    share_dir = get_package_share_directory('ydlidar_ros2_driver')
    parameter_file = LaunchConfiguration('params_file')
    namespace = LaunchConfiguration('namespace')
    node_name = 'ydlidar_ros2_driver_node'

    params_declare = DeclareLaunchArgument(
        'params_file',
        default_value=os.path.join(share_dir, 'params', 'TG.yaml'),
        description='Path to the ROS2 parameters file to use.'
    )

    namespace_declare = DeclareLaunchArgument(
        'namespace',
        default_value='/',
        description='Namespace for the nodes.'
    )

    driver_node = LifecycleNode(
        package='ydlidar_ros2_driver',
        executable='ydlidar_ros2_driver_node',
        name=node_name,
        output='screen',
        emulate_tty=True,
        parameters=[parameter_file],
        namespace=namespace,
        remappings=[
            ('/scan','/echo/scan'),
            ('/tf','/echo/tf'),
            ('/tf_static','/echo/tf_static'),
        ]
    )

    tf2_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_tf_pub_laser',
        arguments=['0', '0', '0.02', '0', '0', '0', '1', 'base_link', 'laser_frame'],
        namespace=namespace,
    )

    return LaunchDescription([
        params_declare,
        namespace_declare,
        driver_node,
        tf2_node,
    ])