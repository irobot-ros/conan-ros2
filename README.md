# conan-ros2

This repository contains Conan recipes for ROS 2 packages and an example application that consumes these recipes.

## Requirements

We provide a Dockerfile that contains all the required dependencies.
To use the Dockerfile:

```sh
bash ./docker/build.sh
bash ./docker/run.sh
```

If you don't want to use the Dockerfile, the following dependencies will have to be installed on your machine:

 - cmake
 - colcon
 - conan
 - lark-parser
 - vcstool
 - wget

## Conan recipes

The `conan` directory contains 4 different Conan recipes.

Two of these recipes are the base for developing any other ROS 2 application in Conan.

 - `ros2-base` is not a stand-alone recipe, but rather a [python requires](https://docs.conan.io/en/1.35/extending/python_requires.html), i.e. a "base class" that provides methods and utilities to be used in other ROS 2 recipes.
 - `ros2-virtualenvgen` this package provides a Conan virtual environment that can be used to expose env variables of all the ROS 2 recipes required by an application.

Then we have two additional recipes that serve as an example of how the base recipes can be used to build and package ROS 2 libraries.

 - `ros2-core` this recipe contains all the core ROS 2 libraries required by C++ applications.
 - `ros2-tf` this recipe contains the ROS 2 TF library C++ implementation.

The `sources` directory contains repos files used by these recipes to fetch all their components.
This is used as an example to show how this approach could directly fetch repositories from the standard url https://github.com/ros2/ros2/blob/foxy/ros2.repos.

Note that the content of these two recipes has been arbirarily chosen for the sake of this example, in order to show that it is possible to have multiple ROS 2 Conan recipes depend on each others.
It is both possible to agglomerate all ROS 2 dependencies within a single ROS 2 recipe as well as have a more fine-grained organization.
As an additional example, it is possible to have a recipe for ROS 2 build tools (e.g. ament), one for the ROS 2 core libraries, one for additional RMW implementations and a last one for desktop tools.
This split allows to cross-compile only those packages that will need to be used and deployed on the robot.

## Example Application

The `example-application` directory contains a basic C++ application that consumes the ROS 2 Conan recipes.
It can be built using standard Conan and CMake commands.

The `example-application/conanfile.py` defines the list of Conan dependencies of the application.
Note that the application is not built as part of the Conan recipe `build` step (which is not present): this allows to better appreciate the use of vanilla CMake.

The `build-example.sh` script can be used to run all the commands required to generate the Conan dependencies, build the application and then finally run it.

```sh
bash build-example.sh
```

The script will generate an executable `example-application/_install/example_app`.
Note that in order to run this application, you first need to source the Conan virtual environment.

```sh
source example-application/_build/conan/activate_ros2.sh
./example-application/_install/example_app
```

#### Using Conan CMake

Note that the `build-example.sh` script invokes the `conan install` command on the `example-application/conanfile.py` in order to grab conan dependencies.
This could be replaced by using the Conan Cmake logic, for example:

```
include (conan)
conan_cmake_run(
    CONANFILE conanfile.py
    INSTALL_FOLDER ${CONAN_FIND_PACKAGE_DIR}
    SETTINGS compiler.libcxx=libstdc++
    SETTINGS arch=${CMAKE_SYSTEM_PROCESSOR}
    BUILD_TYPE Release
)
```
