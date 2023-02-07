from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch.utilities import perform_substitutions
from launch_ros.actions import Node


def launch_setup(context, *args, **kwargs):

    side = perform_substitutions(context, [LaunchConfiguration('side')])

    aruco_marker_publisher_params = {
        'image_is_rectified': True,
        'marker_size': LaunchConfiguration('marker_size'),
        'reference_frame': LaunchConfiguration('reference_frame'),
        'camera_frame': LaunchConfiguration('camera_frame'),
    }

    camera_info_topic = perform_substitutions(
        context, [LaunchConfiguration('camera_info_topic')])

    raw_image_topic = perform_substitutions(
        context, [LaunchConfiguration('raw_image_topic')])

    aruco_marker_publisher = Node(
        package='aruco_ros',
        executable='marker_publisher',
        parameters=[aruco_marker_publisher_params],
        remappings=[('/camera_info', camera_info_topic),
                    ('/image', raw_image_topic)],
    )

    return [aruco_marker_publisher]


def generate_launch_description():

    marker_size_arg = DeclareLaunchArgument(
        'marker_size', default_value='0.05',
        description='Marker size in m. '
    )

    side_arg = DeclareLaunchArgument(
        'side', default_value='left',
        description='Side. ',
        choices=['left', 'right'],
    )

    reference_frame = DeclareLaunchArgument(
        'reference_frame', default_value='base',
        description='Reference frame. '
        'Leave it empty and the pose will be published wrt param parent_name. '
    )

    camera_info_topic_arg = DeclareLaunchArgument(
        'camera_info_topic', default_value='/camera/color/camera_info',
        description='Topic of camera info. ',
    )

    raw_image_topic_arg = DeclareLaunchArgument(
        'raw_image_topic', default_value='/camera/color/image_raw',
        description='Topic of raw color image. ',
    )

    camera_frame_arg = DeclareLaunchArgument(
        'camera_frame', default_value='/camera_link',
        description='Camera frame. '
        'Camera frame name. '
    )

    # Create the launch description and populate
    ld = LaunchDescription()

    ld.add_action(marker_size_arg)
    ld.add_action(side_arg)
    ld.add_action(reference_frame)
    ld.add_action(camera_info_topic_arg)
    ld.add_action(raw_image_topic_arg)
    ld.add_action(camera_frame_arg)

    ld.add_action(OpaqueFunction(function=launch_setup))

    return ld
