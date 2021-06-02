/* Software License Agreement (BSD License)
 *
 *  Copyright (c) 2021, iRobot ROS
 *  All rights reserved.
 *
 *  This file is part of conan-ros2, which is released under BSD-3-Clause.
 *  You may use, distribute and modify this code under the BSD-3-Clause license.
 */

#include <iostream>
#include <rclcpp/rclcpp.hpp>
#include <tf2_ros/static_transform_broadcaster.h>

int main(int argc, char** argv)
{
    rclcpp::init(argc, argv);

    std::cout<<"Hello world"<<std::endl;

    auto node = std::make_shared<rclcpp::Node>("my_node");
    auto static_broadcaster = std::make_unique<tf2_ros::StaticTransformBroadcaster>(node);

    std::vector<geometry_msgs::msg::TransformStamped> static_transforms;
    geometry_msgs::msg::TransformStamped tf_msg;
    tf_msg.header.stamp = node->now();
    tf_msg.transform.translation.x = 1.0;
    static_transforms.push_back(tf_msg);
    static_broadcaster->sendTransform(static_transforms);

    rclcpp::shutdown();

    return 0;
}
