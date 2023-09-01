# Copyright (c) 2023 Ruichao Wu
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch import LaunchDescription
from launch.substitutions import FindExecutable

import yaml
from yaml import SafeLoader

document = """
    header:
      stamp:
        sec: 0
      frame_id: world
    markers:
      - header:
          stamp:
            sec: 0
          frame_id: world
        id: 42
        pose:
          pose:
            position:
              x: -0.17
              y: 0.16
              z: 1.05
            orientation:
              x: 0.710063
              y: 0.704136
              z: -0.00170857
              w: 0.000328001
        confidence: 100.0
      - header:
          stamp:
            sec: 0
          frame_id: world
        id: 43
        pose:
          pose:
            position:
              x: -0.17
              y: -0.10
              z: 1.05
            orientation:
              x: 0.710063
              y: 0.704136
              z: -0.00170857
              w: 0.000328001
        confidence: 100.0
    """


def generate_launch_description():
    ld = LaunchDescription()

    req = yaml.load(document, Loader=SafeLoader)

    cmd_str = 'topic pub -r 10 /marker_publisher/markers aruco_msgs/msg/MarkerArray "{}"'.format(
        str(req)
    )

    ld.add_action(
        ExecuteProcess(cmd=[[FindExecutable(name="ros2"), " {}".format(cmd_str)]], shell=True)
    )
    return ld
