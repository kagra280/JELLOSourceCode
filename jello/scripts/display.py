#!/usr/bin/env python
# Display node: recieves messages from graphics control node and displays them on the screen

import rospy
from std_msgs.msg import String


def info_callback(data):
	#rospy.loginfo("I heard %s", data.data)
	if(data.data in lessons):
		global currInfo
		currInfo = data.data
		#rospy.loginfo(lessons[data.data])

def emote_callback(data):
	#rospy.loginfo("I heard %s", data.data)
	if(data.data in emotes):
		rospy.loginfo("_________________________________________")
		rospy.loginfo(" ")
		rospy.loginfo("                 %s" % emotes[data.data])
		rospy.loginfo(" ")
		rospy.loginfo("           %s" % lessons[currInfo])
		rospy.loginfo(" ")
		rospy.loginfo("_________________________________________")
	else:
		rospy.loginfo("_________________________________________")
		rospy.loginfo(" ")
		rospy.loginfo("                 ^u^ /~")
		rospy.loginfo("               Omedetou~")
		rospy.loginfo("            Congratulations~")
		rospy.loginfo("                  <3")
		rospy.loginfo("_________________________________________")

def display():
	global currInfo
	currInfo = "Konnichiwa"	

	global lessons 
	lessons = {
		"Konnichiwa":"Hello",
		"Nasu":"nasu      eggplant",
		"Daikon":"daikon      radish",
		"Ringo":"ringo       apple",
		"Kyuuri":"kyuuri       cucumber",
		"Suika":"suika       watermelon",
		"Ichigo":"ichigo      strawberry",
		"Ninjin":"ninjin      carrot",
		"Yasai":"yasai        vegetables",
		"Butou":"butou        grapes",
		"Kudamono":"kudamono      fruit",
	}
	global emotes
	emotes = {
		"happy":"'u'",
		"sad":";n;",
		"mad":">n<",
		"surprised":"'o'",
		"peeved":"<~<",
		"content":"'v'",
		"default":"'.'"
	}

	rospy.init_node('display', anonymous=True)
	
	rospy.loginfo("_________________________________________")
	rospy.loginfo(" ")
	rospy.loginfo("                 %s" % emotes["default"])
	rospy.loginfo("             Konnichiwa!")
	rospy.loginfo("           %s" % lessons[currInfo])
	rospy.loginfo(" ")
	rospy.loginfo("_________________________________________")

	rospy.Subscriber("displayInfo", String, info_callback)
	rospy.Subscriber("displayEmote", String, emote_callback)

	rospy.spin()


if __name__ == '__main__':
	rospy.loginfo('Display starting...')


	display()
