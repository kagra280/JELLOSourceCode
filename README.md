# JELLOSourceCode
JELLO is a Japanese language-leaner robot using ROS for Rhodes' Human Robot Interactions course. 
By Jennah Durbin, Dmitry

JELLO (Japanese-English Language Learner - Oto)
-------------------------------------------------------------------
JELLO is a semi-autonomous robot that teaches users basic Japanese.

Packages needed for JELLO:
- PY AIML (Text to speech)
- PocketSphinx (Speech recognition)
- Audio_common 
- Executive_smach
- Scitos Metralabs
- Uashh_smach (State machines)
- find_object_2d (Object recognition)

To start JELLO:
ssh into laptop with ROS kinetic and packages above installed and initialized (excluding object recognition)
Use object recognition software to take pictures of objects in lesson in order used in display.py and control.py

- roslaunch turtlebot_bringup minimal.launch --screen
- roslaunch jello control.launch
- roslaunch jello controls.launch

