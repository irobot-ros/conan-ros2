#!/bin/bash

REPO_DIR=~/conan-ros2

### Build Conan recipes

CONAN_DIR=$REPO_DIR/conan

conan create $CONAN_DIR/ros2-virtualenvgen/all ros2-virtualenvgen/0.0.1@example/stable
conan create $CONAN_DIR/ros2-base/all ros2-base/0.0.1@example/stable
conan create $CONAN_DIR/ros2-core/all ros2-core/foxy@example/stable
conan create $CONAN_DIR/ros2-tf/all ros2-tf/foxy@example/stable

### Build ExampleApplicaton

APP_DIR=$REPO_DIR/example-application
BUILD_DIR=$APP_DIR/_build
BUILD_DIR_CONAN=$BUILD_DIR/conan

conan install $APP_DIR/conanfile.py -if $BUILD_DIR_CONAN
source $BUILD_DIR_CONAN/activate_ros2.sh

cd $BUILD_DIR
cmake -B $BUILD_DIR ..
make
make install
cd -

### Run ExampleApplication

INSTALL_DIR=$APP_DIR/_install

$INSTALL_DIR/example_app
