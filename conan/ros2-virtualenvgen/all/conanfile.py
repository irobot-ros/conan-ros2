import os
import shlex
import subprocess

from conans import ConanFile
from conans.client.generators.virtualenv import VirtualEnvGenerator

_GENERATOR_PKG_NAME = "ros2-virtualenvgen"

class virtualenv_ros2(VirtualEnvGenerator):
    name = "virtualenv_ros2"
    suffix = "_ros2"
    venv_name = "conanenvros2"

    # These are the env variables that are exposed by ROS 2 workspaces
    # Note: we ignore PATH because we don't want conan requirements to expose it.
    ROS2_PATHS_VARS = [
        "AMENT_PREFIX_PATH",
        "CMAKE_PREFIX_PATH",
        "COLCON_PREFIX_PATH",
        "LD_LIBRARY_PATH",
        "PKG_CONFIG_PATH",
        "PYTHONPATH",
    ]

    def _update_env_paths(self, key, new_paths, package_path):
        new_paths = new_paths.strip()

        if key in self.env:
            current_paths = self.env[key]
        else:
            current_paths = []

        for p in new_paths.split(os.pathsep):
            # Ignore paths that are not pointing to this specific conan dependency
            if not p.startswith(package_path):
                continue

            # Do not add duplicated paths in the list
            if p in current_paths:
                continue

            # Add new path at the beginning of the list
            current_paths.insert(0, p)

        # Update env
        self.env.update({key: current_paths})

    def __init__(self, conanfile):
        super(virtualenv_ros2, self).__init__(conanfile)

        # Reset env as we only want to include ROS 2 variables
        self.env = {}

        # Get deps_cpp_info from conanfile invoking this generator
        for dep_name, dep_cpp_info in self.deps_build_info.dependencies:

            # This custom generator is specified as a dependency, so skip it
            if _GENERATOR_PKG_NAME == dep_name:
                continue

            package_path = dep_cpp_info.rootpath
            setup_script_path = os.path.join(package_path, "local_setup.bash")

            # Ignore dependencies that do not provide a setup script
            if not os.path.isfile(setup_script_path):
                continue

            # We found a dependency that provides a ROS 2 setup script.
            # Source the script in a separate shell and grab the env variables that it sets.
            # These env variables will be pushed into the conan env and then dumped to virtual env script.
            command = "bash -c 'source {script} && env'".format(script=setup_script_path)
            command = shlex.split(command)
            proc = subprocess.Popen(command, stdout=subprocess.PIPE)
            for line in proc.stdout:
                (key, _, value) = line.decode().partition("=")
                # Consider only env variables that are related to ROS 2
                if key in self.ROS2_PATHS_VARS:
                    self._update_env_paths(key, value, package_path)

            proc.communicate()

class VirtualEnvRos2GeneratorPackage(ConanFile):
    name = _GENERATOR_PKG_NAME
    version = "0.0.1"
    license = "Apache 2.0"
    url = "https://index.ros.org/doc/ros2/"
    homepage = "https://index.ros.org/doc/ros2/"
    description = "Conan generator wrapping ROS 2 setup scripts"
