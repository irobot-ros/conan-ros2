# Software License Agreement (BSD License)
#
#  Copyright (c) 2021, iRobot ROS
#  All rights reserved.
#
#  This file is part of conan-ros2, which is released under BSD-3-Clause.
#  You may use, distribute and modify this code under the BSD-3-Clause license.
#

import os
import sys

from conans import ConanFile, errors, tools

class Ros2Base(object):
    options = {"python_version": "ANY"}

    @property
    def _workspace_dir(self):
        """Default name for the ROS 2 workspace directory"""
        return "_ws"

    @property
    def _source_dir(self):
        """Default name for the sources directory in a ROS 2 workspace"""
        return "src"

    @property
    def _build_dir(self):
        """Default name for the build directory in a ROS 2 workspace"""
        return "build"

    @property
    def _install_dir(self):
        """Default name for the install directory in a ROS 2 workspace"""
        return "install"

    @property
    def _python_version(self):
        """The currently used Python version as a string"""
        return "python{major}.{minor}".format(major=sys.version_info[0], minor=sys.version_info[1])

    def _clean_workspace(self, workspace_dir):
        """Ensures that a directory is empty by removing and re-creating it"""
        tools.rmdir(workspace_dir)
        tools.mkdir(workspace_dir)

    def _import_repositories(self, source_dir, repos_file, strict=True):
        """
        Given a .repos file, uses vcs tool to import all the repositories into source_dir.
        If the strict flag is set to True, it raises an error if the .repos file is not found.
        """
        if os.path.isfile(repos_file):
            tools.mkdir(source_dir)
            self.run("vcs import {src_dir} < {repos_file}".format(src_dir=source_dir, repos_file=repos_file))
        elif strict:
            raise OSError("repository file not found")

    def _colcon_ignore_packages(self, workspace_dir, ignore_list):
        """
        Given a list of directories relative to workspace_dir, adds an empty file named
        COLCON_IGNORE in each of them. The colcon build tool looks for these files and skips
        the directories where they are found.
        """
        with tools.chdir(workspace_dir):
            for ignore_item in ignore_list:
                # Note: tools.touch can't be used here as we need to create the files
                self.run("touch {file}".format(file=ignore_item))

    def _generate_cmake_toolchain_arg(self, root_paths):
        """
        Returns a string containing a CMake command line option pointing to a CMake toolchain file.
        """
        # This method is invoked by the ROS 2 recipes that have this one as python require.
        # This is basically a path to this package
        toolchain_file_path = os.path.join(self.python_requires["ros2-base"].path, "generic_linux.cmake")
        # Allow toolchain to know where the ROS workspaces are
        # This needs to be specified as a CMake list, so use ";" as a separator
        os.environ["ROS2_CONAN_WORKSPACE"] = root_paths.replace(os.pathsep, ";")
        return "-DCMAKE_TOOLCHAIN_FILE={toolchain}".format(toolchain=toolchain_file_path)

    def _export_ros2_env_var(self, dep_cpp_info):
        """
        Adds a ROS 2 dependency to the relevant environment variable.
        This utility is needed because when using double profiles in Conan, only build_requirements
        expose their environment.
        """
        for env_var in ("AMENT_PREFIX_PATH", "CMAKE_PREFIX_PATH", "COLCON_PREFIX_PATH"):
            if env_var in os.environ:
                os.environ[env_var] = dep_cpp_info.rootpath + os.pathsep + os.environ[env_var]
            else:
                os.environ[env_var] = dep_cpp_info.rootpath

        python_dir = os.path.join(dep_cpp_info.rootpath, "lib", self._python_version, "site-packages")
        pythonpath_var = "PYTHONPATH"
        if os.path.isdir(python_dir):
            if pythonpath_var in os.environ:
                os.environ[pythonpath_var] = python_dir + os.pathsep + os.environ[pythonpath_var]
            else:
                os.environ[pythonpath_var] = python_dir

    def _colcon_build(self, workspace_path = ".", cmake_args = []):
        """
        Builds a ROS 2 workspace using the colcon build tool. The provided CMake arguments are added
        to some default colcon arguments.
        """
        colcon_args = [
            "--merge-install",
            "--cmake-force-configure",
        ]

        if cmake_args:
            cmake_args_string = ' '.join(cmake_args)
            colcon_args.append("--cmake-args {args}".format(args=cmake_args_string))

        colcon_args_string = ' '.join(colcon_args)

        # Run the colcon command inside the workspace directory
        with tools.chdir(workspace_path):
            self.run("colcon build {args}".format(args=colcon_args_string))

    def _replace_python_shebangs(self, python_scripts_dir, python_version):
        """
        Replaces the Python shebang that Setuptools adds to Python scripts entry points, as that one may use
        the absolute paths and this makes the scripts non-relocatable.
        Several discussions on the web, e.g. https://stackoverflow.com/questions/1530702/dont-touch-my-shebang 
        """
        virtual_env_shebang = "#!{python_executable}".format(python_executable=sys.executable)
        absolute_path_shebang = "#!/usr/bin/python3"
        generic_python_shebang = "#!/usr/bin/env {python_version}".format(python_version=python_version)
        if os.path.isdir(python_scripts_dir):
            for filename in os.listdir(python_scripts_dir):
                filepath = os.path.join(python_scripts_dir, filename)
                tools.replace_in_file(filepath, virtual_env_shebang, generic_python_shebang, strict=False)
                tools.replace_in_file(filepath, absolute_path_shebang, generic_python_shebang, strict=False)

    def configure(self):
        # The ROS 2 packages contains some python3 modules that are only compatible with the python version used to create the package.
        # We add this dummy Conan option to encode the supported python version on the package metadata.
        if self.options.python_version and self.options.python_version != self._python_version:
            raise errors.ConanInvalidConfiguration("Do not set Python version option, Conan will automatically detect the one used to build the package")
        self.options.python_version = self._python_version

    def system_requirements(self):
        if self.settings.os == "Linux" and tools.os_info.is_linux:
            package_tool = tools.SystemPackageTool()
            packages = ['python3-colcon-common-extensions', 'python3-vcstool']

            for package in packages:
                package_tool.install(package)
                if not package_tool.installed(package):
                    raise errors.ConanInvalidConfiguration("ROS 2 requires {}.".format(package))

    def package(self):
        install_dir_path = os.path.join(self._workspace_dir, self._install_dir)

        # Post build patch
        ros2_bin_dir = os.path.join(install_dir_path, "bin")
        self._replace_python_shebangs(ros2_bin_dir, self._python_version)

        self.copy("*", dst="./", src=install_dir_path)
        tools.rmdir(self._workspace_dir)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

        self.env_info.AMENT_PREFIX_PATH.append(self.package_folder)
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)
        self.env_info.COLCON_PREFIX_PATH.append(self.package_folder)

        python_dir = os.path.join(self.package_folder, "lib", self._python_version, "site-packages")
        if os.path.isdir(python_dir):
            self.env_info.PYTHONPATH.append(python_dir)

class Ros2BaseReq(ConanFile):
    name = "ros2-base"
    version = "0.0.1"
    license = "Apache 2.0"
    url = "https://index.ros.org/doc/ros2/"
    homepage = "https://index.ros.org/doc/ros2/"
    description = "Python requires for ROS 2 conan recipes"

    exports = ["generic_linux.cmake"]
