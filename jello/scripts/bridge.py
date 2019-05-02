#!/usr/bin/env python
import rospy

from std_msgs.msg import Float32MultiArray

rospy.init_node('bridge')

def callback(msg):
    if len(msg.data) != 0:
        pub.publish(msg)

sub = rospy.Subscriber('objects', Float32MultiArray, callback)
pub = rospy.Publisher('bridge/objects', Float32MultiArray, queue_size=10)

rospy.spin()
