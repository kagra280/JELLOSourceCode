#!/usr/bin/env python
import rospy
from std_msgs.msg import String

rospy.init_node('speech_recognition')
rospy.loginfo("Initializing speech recognition node")
pub = rospy.Publisher('userSpeech', String, queue_size=10)
r = rospy.Rate(1)

def get_speech(data):
  speech_text = data.data
  rospy.loginfo("You said:: %s",speech_text)
  pub.publish(speech_text)

def listener():
  rospy.loginfo("Starting Speech Recognition")
  rospy.Subscriber("kws_data", String, get_speech)
  rospy.spin()

while not rospy.is_shutdown():
  listener()
