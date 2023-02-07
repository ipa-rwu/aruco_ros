from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch.utilities import perform_substitutions
from launch_ros.actions import Node


def launch_setup(context, *args, **kwargs):

    eye = perform_substitutions(context, [LaunchConfiguration('eye')])

    aruco_single_params = {
        'image_is_rectified': True,
        'marker_size': LaunchConfiguration('marker_size'),
        'marker_id': LaunchConfiguration('marker_id'),
        'reference_frame': LaunchConfiguration('reference_frame'),
        'camera_frame': LaunchConfiguration('camera_frame'),
        'marker_frame': LaunchConfiguration('marker_frame'),
        'corner_refinement': LaunchConfiguration('corner_refinement'),
    }
    camera_info_topic = perform_substitutions(
        context, [LaunchConfiguration('camera_info_topic')])

    raw_image_topic = perform_substitutions(
        context, [LaunchConfiguration('raw_image_topic')])

    aruco_single = Node(
        package='aruco_ros',
        executable='single',
        parameters=[aruco_single_params],
        remappings=[('/camera_info', camera_info_topic),
                    ('/image', raw_image_topic)],
    )

    return [aruco_single]


def generate_launch_description():

    marker_id_arg = DeclareLaunchArgument(
        'marker_id', default_value='582',
        description='Marker ID. '
    )

    marker_size_arg = DeclareLaunchArgument(
        'marker_size', default_value='0.34',
        description='Marker size in m. '
    )

    eye_arg = DeclareLaunchArgument(
        'eye', default_value='left',
        description='Eye. ',
        choices=['left', 'right'],
    )

    marker_frame_arg = DeclareLaunchArgument(
        'marker_frame', default_value='aruco_marker_frame',
        description='Frame in which the marker pose will be refered. '
    )

    reference_frame = DeclareLaunchArgument(
        'reference_frame', default_value='',
        description='Reference frame. '
        'Leave it empty and the pose will be published wrt param parent_name. '
    )

    corner_refinement_arg = DeclareLaunchArgument(
        'corner_refinement', default_value='LINES',
        description='Corner Refinement. ',
        choices=['NONE', 'HARRIS', 'LINES', 'SUBPIX'],
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

    ld.add_action(marker_id_arg)
    ld.add_action(marker_size_arg)
    ld.add_action(eye_arg)
    ld.add_action(marker_frame_arg)
    ld.add_action(reference_frame)
    ld.add_action(corner_refinement_arg)
    ld.add_action(camera_info_topic_arg)
    ld.add_action(raw_image_topic_arg)
    ld.add_action(camera_frame_arg)

    ld.add_action(OpaqueFunction(function=launch_setup))

    return ld
