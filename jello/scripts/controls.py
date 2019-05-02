#!/usr/bin/env python
import roslib; roslib.load_manifest('uashh_smach')

import rospy

from smach import State, StateMachine
from smach_ros import SimpleActionState
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import String, Bool
import uashh_smach.util as util
from uashh_smach.util import WaitForMsgState

class ObjectRecognitionState(WaitForMsgState):
    def __init__(self):
        WaitForMsgState.__init__(self, 'bridge/objects', Float32MultiArray, self._msg_cb, input_keys=['objects_in'], output_keys=['recognized_object'])
        self.response_pub = rospy.Publisher('response', String, queue_size=10)

    def _msg_cb(self, msg, ud):
        ud.recognized_object = ud.objects_in[int(msg.data[0]) - 10]
        self.response_pub.publish(ud.objects_in[int(msg.data[0]) - 10])
        #rospy.sleep(3)
        #if msg.data[0] == ud.goal_object:
            #ud.id = msg.data[0]
            #return True
        #return False

class SpeechDetectionState(WaitForMsgState):
    def __init__(self):
        WaitForMsgState.__init__(self, 'userSpeech', String, self._msg_cb, input_keys=['current_object', 'words'], output_keys=['word_recognized'])
        self.chatter_pub = rospy.Publisher('chatter', String, queue_size=10)
        self.emotes_pub = rospy.Publisher('emotes', String, queue_size=10)

    def _msg_cb(self, msg, ud):
        if msg.data.strip() == ud.current_object:
            self.emotes_pub.publish('correct')
            return True
        self.emotes_pub.publish('incorrect')
        return False
        #    self.chatter_pub.publish('USER INCORRECT ' + msg.data)
        #    self.emotes_pub.publish('neutral')
            #self.mutex.acquire()
            #self.mutex.release()
        #    return False
        #ud.word_recognized = msg.data
        #return True



if __name__ == '__main__':
    rospy.init_node('control')
    #pub = rospy.Publisher('moveComplete', String, queue_size=10)

    control = StateMachine(outcomes=['succeeded','aborted','preempted'])
    control.userdata.objects = ['konnichiwa', 'fruits', 'apple', 'grapes', 'strawberry', 'eggplant', 'carrots', 'cucumber', 'vegetables', 'michael', 'vegetables']
    #control.userdata.objectID = 1.0
    control.userdata.numberOfTrials = 0
    with control:
        def goal_object_cb(userdata, goal):
            if counter_in == 10: #11?
                ud.counter_out = 0
            else:
                ud.counter_out = ud.counter_in + 1

            goal_object = MoveBaseGoal()
            goal_object.target_pose.header.frame_id = 'map'
            goal_object.target_pose.pose.position.x = ud.objects[counter_in][0][0]
            goal_object.target_pose.pose.position.y = ud.objects[counter_in][0][1]
            goal_object.target_pose.pose.position.z = 0.0
            goal_object.target_pose.pose.orientation.x = ud.objects[counter_in][1][0]
            goal_object.target_pose.pose.orientation.y = ud.objects[counter_in][1][1]
            goal_object.target_pose.pose.orientation.z = ud.objects[counter_in][1][2]
            goal_object.target_pose.pose.orientation.w = ud.objects[counter_in][1][3]

            return goal_object

        #StateMachine.add('MOVE', SimpleActionState('move_base', MoveBaseAction, goal_cb=goal_object_cb, input_keys=['goal_objects','counter_in'], output_keys=['counter_out']),
        #                        transitions={'succeeded':'OBJECTRECOGNITION', 'aborted':'aborted', 'preempted':'preempted'},
        #                        remapping={'goal_objects':'objects', 'counter_in':'counter', 'counter_out':'counter'})
        StateMachine.add('OBJECTRECOGNITION', ObjectRecognitionState(), transitions={'succeeded':'SPEECHDETECTION', 'aborted':'aborted', 'preempted':'preempted'},
                                                                        remapping={'objects_in':'objects', 'recognized_object':'object'})
        #StateMachine.add('SPEECHCOMPLETE', WaitForMsgState('speechComplete', String, timeout=3), transitions={'succeeded':'SPEECHDETECTION', 'aborted':'aborted', 'preempted':'preempted'})
        StateMachine.add('SPEECHDETECTION', SpeechDetectionState(), transitions={'succeeded':'OBJECTRECOGNITION', 'aborted':'SPEECHDETECTION', 'preempted':'preempted'},
                                                                        remapping={'current_object':'object','words':'objects', 'word_recognized':'word'})
        #StateMachine.add('MOVE', SpeechRecognitionState(), transitions={'succeeded':'OBJECTRECOGNITION', 'aborted':'MOVE', 'forwarded':'succeeded'},
                                                                        #remapping={'current_word':'word', 'current_object':'object', 'inputNumberOfTrials':'numberOfTrials', 'outputNumberOfTrials':'numberOfTrials'})
    control.execute()
