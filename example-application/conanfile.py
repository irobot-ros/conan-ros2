from conans import ConanFile

class ExampleApplicationConan(ConanFile):
    name = "ExampleApplication"
    version = "1.0.0"
    generators = ["cmake_find_package", "cmake", "virtualenv_ros2"]

    def build_requirements(self):
        self.build_requires("ros2-virtualenvgen/0.0.1@example/stable")

    def requirements(self):
        self.requires("ros2-core/foxy@example/stable")
        self.requires("ros2-tf/foxy@example/stable")
