#!/usr/bin/env python

import socket
import struct
import rospy
from sensor_msgs.msg import Imu
import tf
import math

# Parameters - TODO make them CLI/ROS-Parameters

UDP_IP = "192.168.0.109"
UDP_PORT = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind((UDP_IP, UDP_PORT))
closeSocket = False


class RosNode:
    def __init__(self):
        rospy.init_node("ros_node")
        rospy.loginfo("Starting RosNode.")
        self.message_pub = rospy.Publisher("imu_data", Imu, queue_size=10)
        self.rate = rospy.Rate(100)
        pass


if __name__ == "__main__":
    ros_node = RosNode()
    imu_data = Imu()

    while not rospy.is_shutdown():
        try:
            data, addr = sock.recvfrom(8192)

            if data and not closeSocket:
                rospy.loginfo("Recieving Socket Data")
                closeSocket = True

            # list = data.split(",")
            # values = struct.unpack('<ddddd', data)
            # rospy.loginfo(value)
            #sensor_array = []
            sensor_array = list(map(float, data.split(",")))
            #for i in list:
            #    sensor_array.append(float(i))
                # if sensor_array[5:]:
                #     print(sensor_array[5:])
                #     continue
            # print(data)
            quaternion = tf.transformations.quaternion_from_euler(
                math.radians(sensor_array[0]), math.radians(sensor_array[1]), math.radians(sensor_array[2]))
            # print(quaternion)
            # print(quaternion[2])
            imu_data.header.frame_id = "/imu"
            imu_data.header.stamp = rospy.Time.now()
            imu_data.orientation.x = quaternion[0]
            imu_data.orientation.y = quaternion[1]
            imu_data.orientation.z = quaternion[2]
            imu_data.orientation.w = quaternion[3]
            imu_data.angular_velocity.x = sensor_array[3]
            imu_data.angular_velocity.y = sensor_array[4]
            imu_data.angular_velocity.z = sensor_array[5]
            imu_data.linear_acceleration.x = sensor_array[6]
            imu_data.linear_acceleration.y = sensor_array[7]
            imu_data.linear_acceleration.z = sensor_array[8]

            ros_node.message_pub.publish(imu_data)
            ros_node.rate.sleep()
            # print(sensor_array)
        except socket.error as e:
            rospy.loginfo("RosNode and UDP Socket Shutting Down")
            sock.close()
            print(e)
