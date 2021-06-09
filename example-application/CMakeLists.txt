cmake_minimum_required(VERSION 3.5)

project(example_application)

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
    set(CMAKE_CXX_STANDARD 14)
endif()

find_package(rclcpp REQUIRED)
find_package(tf2_ros REQUIRED)

add_executable(example_app main.cpp)
target_link_libraries(example_app PRIVATE rclcpp::rclcpp tf2_ros::tf2_ros)

install(
    TARGETS example_app
    DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/_install
)
