import os
import shutil
from conans import ConanFile, load, tools

class Ros2CoreConan(ConanFile):
    name = "ros2-core"
    license = "Apache 2.0"
    url = "https://index.ros.org/doc/ros2/"
    homepage = "https://index.ros.org/doc/ros2/"
    description = "ROS 2 core libraries"
    settings = "os", "compiler", "build_type", "arch"

    exports = ["ignore_list"]
    generators = "cmake_find_package"

    python_requires = "ros2-base/0.0.1@example/stable"
    python_requires_extend = "ros2-base.Ros2Base"

    def init(self):
        # Additional recipe options must be added here!
        base = self.python_requires["ros2-base"].module.Ros2Base
        self.options = base.options

    def requirements(self):
        self.requires("spdlog/1.8.5")
        self.requires("tinyxml2/8.0.0")

    def source(self):
        # Make sure that we have an empty workspace directory
        workspace_path = os.path.abspath(self._workspace_dir)
        self._clean_workspace(workspace_path)

        repos_file_url = self.conan_data["sources"][self.version]["url"]
        repos_file_path = os.path.join(workspace_path, "ros2.repos")
        tools.download(repos_file_url, filename=repos_file_path)

        source_path = os.path.join(workspace_path, self._source_dir)
        self._import_repositories(source_path, repos_file_path)

    def build(self):

        workspace_path = os.path.join(self.build_folder, self._workspace_dir)

        # Optional: ignore version-specific packages.
        colcon_ignore_file = "ignore_list"
        if os.path.isfile(colcon_ignore_file):
            content = load(colcon_ignore_file)
            files_list = content.splitlines()
            self._colcon_ignore_packages(workspace_path, files_list)

        # Replace the ROS FindTinyXML2 file with the conan one
        # TODO: figure out if there is a better way to do this:
        conan_find_tinyxml2 = os.path.join(self.build_folder, "Findtinyxml2.cmake") # TODO: this should be named correctly!
        ros_find_tinyxml2 = os.path.join(workspace_path, "src/ros2/tinyxml2_vendor/cmake/Modules/FindTinyXML2.cmake")
        shutil.copyfile(conan_find_tinyxml2, ros_find_tinyxml2)

        cmake_args = [
            "-DTHIRDPARTY:BOOL=ON",
            "-DBUILD_TESTING:BOOL=OFF",
        ]

        # Cross-compilation specific flags
        if tools.cross_building(self.settings):
            ros2_dependencies_paths = workspace_path
            if "AMENT_PREFIX_PATH" in os.environ:
                ros2_dependencies_paths += os.pathsep + os.environ["AMENT_PREFIX_PATH"]
            cmake_toolchain_arg = self._generate_cmake_toolchain_arg(ros2_dependencies_paths)
            cmake_args.append(cmake_toolchain_arg)

        # Invoke colcon on the workspace
        self._colcon_build(workspace_path, cmake_args)
