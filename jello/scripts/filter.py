#!/usr/bin/env python
import rospy

from std_msgs.msg import String

words = ['apple', 'banana']

rospy.init_node('filter')

def callback(msg):
    if msg.data in words:
        pub.publish(msg)

sub = rospy.Subscriber('userSpeech', String, callback)
pub = rospy.Publisher('words', String, queue_size=10)

rospy.spin()
