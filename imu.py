#!/usr/bin/env python

import socket
import struct
import rospy
from geometry_msgs.msg import PoseStamped

# Parameters - TODO make them CLI/ROS-Parameters
UDP_IP = "192.168.0.109"
UDP_PORT = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind((UDP_IP, UDP_PORT))


def talker():

    while not rospy.is_shutdown():
        data, addr = sock.recvfrom(8192)  # buffer size is 7*8 bytes
        list = data.split(",")
        # values = struct.unpack('<ddddd', data)
        # rospy.loginfo(value)
        sensor_array = []
        for i in list:
            sensor_array.append(float(i))
            # if sensor_array[5:]:
            #     print(sensor_array[5:])
            #     continue
        # print(data)
        print(data)
        # print(sensor_array)
        # print(values)


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
