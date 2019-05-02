#!/usr/bin/env python
# ScreenInfo recieves messages from the display controller and sends the correct text info to send to the display node

import rospy
from std_msgs.msg import String


def chatter_callback(data):

	lessonEng = ['hello', 'fruits', 'apple', 'grapes', 'strawberry', 'watermellon', 'vegetables', 'eggplant', 'carrots', 'cucumber', 'radish']
	lessonJpn = ['konnichiwa', 'kudamono', 'ringo', 'budou', 'ichigo', 'suika', 'yasai', 'nasu', 'ninjin', 'kyuuri', 'daikon']
	allLessons = [lessonEng, lessonJpn]
	global currentWord

	dataList = data.data.split()

	if dataList[1] == "CORRECT":  #User is right
		#rospy.loginfo("screenInfo: Correct! %s " % data.data)
		currentWord = currentWord + 1
		if currentWord >= len(allLessons[0]):
			currentWord = 0
			rospy.loginfo("Next lesson")
			return
		pub = rospy.Publisher('displayInfo', String, queue_size=10)
        	pub.publish(allLessons[1][currentWord]) #Publish the Japanese word
        	#rospy.loginfo(test_str)
	else:
		pub = rospy.Publisher('displayInfo', String, queue_size=10)
        	pub.publish(allLessons[1][currentWord])
		
		



def screenInfo():

	rospy.init_node('screenInfo', anonymous=True)
	global currentWord 
	currentWord = 0


        rospy.Subscriber("chatter", String, chatter_callback)
        rate = rospy.Rate(10)
        #while not rospy.is_shutdown():
                #rate.sleep()
        rospy.spin()

if __name__ == '__main__':

	

	try:
		screenInfo()
	except rospy.ROSInterruptException:
		pass
