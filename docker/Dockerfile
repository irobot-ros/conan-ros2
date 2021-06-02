FROM ubuntu:20.04
MAINTAINER Alberto Soragna asoragna at irobot dot com

# working directory
ENV HOME /root
WORKDIR $HOME

# Locale options
RUN apt-get update && apt-get install -y locales
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y \
    curl \
    git \
    gnupg2 \
    lsb-release \
    python3-pip \
    python3-dev \
    wget

RUN pip3 install --upgrade pip

RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key  -o /usr/share/keyrings/ros-archive-keyring.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null

RUN apt-get update && apt-get install -y \
    cmake \
    python3-colcon-common-extensions \
    python3-vcstool

RUN pip3 install -U \
    conan \
    lark-parser
