#!/usr/bin/env python
# ScreenEmotes recieves messages from the display controller and sends the correct emotes to send to the display node

import rospy
import random
from std_msgs.msg import String



def emotes_callback(data):

	wrongEmotes = ["sad", "mad", "peeved"]
	rightEmotes = ["happy", "surprised", "content"]
	#rospy.loginfo(data.data)
	pub = rospy.Publisher('displayEmote', String, queue_size=10)

	if data.data == "incorrect":
        	pub.publish(random.choice(wrongEmotes))
        	#rospy.loginfo(test_str)
	elif data.data == "correct":
        	pub.publish(random.choice(rightEmotes))
	else:
		pub.publish("neutral")



def screenEmote():

	rospy.init_node('screenEmotes', anonymous=True)
        rospy.Subscriber("emotes", String, emotes_callback)
        rate = rospy.Rate(10)
        #while not rospy.is_shutdown():
                #rate.sleep()
        rospy.spin()



if __name__ == '__main__':
	
	try:
		screenEmote()
	except rospy.ROSInterruptException:
		pass
