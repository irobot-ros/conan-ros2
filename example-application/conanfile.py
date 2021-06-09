# Software License Agreement (BSD License)
#
#  Copyright (c) 2021, iRobot ROS
#  All rights reserved.
#
#  This file is part of conan-ros2, which is released under BSD-3-Clause.
#  You may use, distribute and modify this code under the BSD-3-Clause license.
#

from conans import ConanFile

class ExampleApplicationConan(ConanFile):
    name = "ExampleApplication"
    version = "1.0.0"
    generators = ["virtualenv_ros2"]

    def build_requirements(self):
        self.build_requires("ros2-virtualenvgen/0.0.1@example/stable")

    def requirements(self):
        self.requires("ros2-core/foxy@example/stable")
        self.requires("ros2-tf/foxy@example/stable")
