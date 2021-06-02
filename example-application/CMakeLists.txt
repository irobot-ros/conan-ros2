cmake_minimum_required(VERSION 3.5)

project(example_application)

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
    set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Include the output of the 'cmake' conan generator.
include(/root/conan-ros2/example-application/_build/conan/conanbuildinfo.cmake)

find_package(rclcpp REQUIRED)
find_package(tf2_ros REQUIRED)

add_executable(example_app main.cpp)
target_link_libraries(example_app PRIVATE rclcpp::rclcpp tf2_ros::tf2_ros)

install(
    TARGETS example_app
    DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/_install
)
