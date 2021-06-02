#!/bin/bash

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

docker run -it --rm \
	  --net=host \
	  --privileged \
	  -v $THIS_DIR/../:/root/conan-ros2 \
	  conan_ros2_example \
	  bash
