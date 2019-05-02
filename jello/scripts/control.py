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
        ud.object = objects[msg.data[0]]
        self.response_pub.publish(ud.object)

        #if msg.data[0] == ud.goal_object:
            #ud.id = msg.data[0]
            #return True
        #return False

class SpeechDetectionState(WaitForMsgState):
    def __init__(self):
        WaitForMsgState.__init__(self, 'userSpeech', String, self._msg_cb, input_keys=['words'], output_keys=['word_recognized'], timeout=20)
        self.chatter_pub = rospy.Publisher('chatter', String, queue_size=10)
        self.emotes_pub = rospy.Publisher('emotes', String, queue_size=10)


    def _msg_cb(self, msg, ud):
        if msg.data not in words:
            self.chatter_pub.publish('USER INCORRECT ' + userdata.current_object) # Need current object
            self.emotes_pub.publish('neutral')
            #self.mutex.acquire()
            #self.mutex.release()
            return False

        ud.word_recognized = msg.data
        return True

class SpeechRecognitionState(State):
    def __init__(self):
        State.__init__(self, outcomes=['succeeded', 'aborted', 'forwarded'], input_keys=['current_word', 'current_object', 'inputNumberOfTrials'], output_keys=['outputNumberOfTrials'])
        self.emotes_pub = rospy.Publisher('emotes', String, queue_size=10)
        self.chatter_pub = rospy.Publisher('chatter', String, queue_size=10)


    def execute(self, userdata):
        if userdata.inputNumberOfTrials == 3:
            self.emotes_pub.publish('neutral')
            return 'forwarded'
        if userdata.current_word == userdata.current_object:
            self.emotes_pub.publish('correct')
            self.chatter_pub.publish('USER CORRECT ' + userdata.current_word.upper())
            return 'succeeded'
        userdata.outputNumberOfTrials = userdata.inputNumberOfTrials + 1
        self.emotes_pub.publish('incorrect')
        self.chatter_pub.publish('USER INCORRECT ' + userdata.current_word) # Need current object
        #self.mutex.acquire()
        #self.mutex.release()
        return 'aborted'

if __name__ == '__main__':
    rospy.init_node('control')
    #pub = rospy.Publisher('moveComplete', String, queue_size=10)

    control = StateMachine(outcomes=['succeeded','aborted','preempted'])
    control.userdata.objectsEng = ['hello', 'fruits', 'apple', 'grapes', 'strawberry', 'watermellon', 'vegetables', 'eggplant', 'carrots', 'cucumber', 'radish']
    control.userdata.objectsJpn = ['konnichiwa', 'kudamono', 'ringo', 'budou', 'ichigo', 'suika', 'yasai', 'nasu', 'ninjin', 'kyuuri', 'daikon']
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
        #                        remapping={'goal_objects':'objectsEng', 'counter_in':'counter', 'counter_out':'counter'})
        StateMachine.add('OBJECTRECOGNITION', ObjectRecognitionState(), transitions={'succeeded':'SPEECHCOMPLETE', 'aborted':'OBJECTRECOGNITION', 'preempted':'preempted'}, #object recog back to move
                                                                        remapping={'objects_in':'objectsEng', 'objects_in_J':'objectsJpn', 'recognized_object':'object'})
        StateMachine.add('SPEECHCOMPLETE', WaitForMsgState('speechComplete', Bool, timeout=3), transitions={'succeeded':'SPEECHDETECTION', 'aborted':'SPEECHRECOGNITION', 'preempted':'preempted'})
        StateMachine.add('SPEECHDETECTION', SpeechDetectionState(), transitions={'succeeded':'SPEECHRECOGNITION', 'aborted':'aborted', 'preempted':'preempted'},
                                                                        remapping={'words':'objectsJpn', 'word_recognized':'word'})
        StateMachine.add('SPEECHRECOGNITION', SpeechRecognitionState(), transitions={'succeeded':'OBJECTRECOGNITION', 'aborted':'SPEECHDETECTION', 'forwarded':'OBJECTRECOGNITION'}, #object recog back to move
                                                                        remapping={'current_word':'word', 'current_object':'object', 'inputNumberOfTrials':'numberOfTrials', 'outputNumberOfTrials':'numberOfTrials'})
    control.execute()
