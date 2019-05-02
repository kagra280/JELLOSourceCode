#!/usr/bin/env python
import roslib; roslib.load_manifest('uashh_smach')

import rospy

from smach import StateMachine
from smach_ros import SimpleActionState
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import Float32MultiArray
import uashh_smach.util as util
from uashh_smach.util import WaitForMsgState

if __name__ == '__main__':
    rospy.init_node('control')
    control = StateMachine(outcomes=['succeeded','aborted','preempted'])
    with control:
        StateMachine.add('RECOGNITION', WaitForMsgState('move', Bool), transitions={'succeeded':'succeeded', 'aborted':'aborted', 'preempted':'preempted'})
    control.execute()
