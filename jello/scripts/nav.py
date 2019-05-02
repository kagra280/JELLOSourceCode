#!/usr/bin/env python

import rospy
import actionlib
from smach import State, StateMachine
from std_msgs.msg import Float32MultiArray
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

waypoints = [
    ['one', (3.189, -0.857), (0.0, 0.0, -0.116, 0.993)],
    ['two', (1.871, -1.107), (0.0, 0.0, 0.997, 0.077)]
]

class Waypoint(State):
    def __init__(self, position, orientation, objectID):
        State.__init__(self, outcomes=['succeeded'])

        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.client.wait_for_server()

        self.goal = MoveBaseGoal()
        self.goal.target_pose.header.frame_id = 'map'
        self.goal.target_pose.pose.position.x = position[0]
        self.goal.target_pose.pose.position.y = position[1]
        self.goal.target_pose.pose.position.z = 0.0
        self.goal.target_pose.pose.orientation.x = orientation[0]
        self.goal.target_pose.pose.orientation.y = orientation[1]
        self.goal.target_pose.pose.orientation.z = orientation[2]
        self.goal.target_pose.pose.orientation.w = orientation[3]

	self.recognized = True
	self.objectID = objectID

    def objects_callback(self, objects):
        if objects.data and objects.data[0] == 4:
            self.recognized = True

    def execute(self, objectID):
	self.recognized = False
        self.sub = rospy.Subscriber('objects', Float32MultiArray, self.objects_callback)
        self.client.send_goal(self.goal)
        self.client.wait_for_result()
        if self.recognized == True:
            rospy.loginfo("recognized")
	return 'succeeded'

if __name__ == '__main__':
    rospy.init_node('patrol')

    patrol = StateMachine('succeeded')
    with patrol:
        for i,w in enumerate(waypoints):
            StateMachine.add(w[0],
                              Waypoint(w[1], w[2], 4),
                              transitions={'succeeded' :waypoints[(i + 1) % len(waypoints)][0]})
	

    patrol.execute()
