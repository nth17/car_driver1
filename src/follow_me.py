#!/usr//bin/env python

import rospy
from std_msgs.msg import Int32
from std_msgs.msg import String



#back = rospy.Subscriber('/car/get_back', Int32, chk_back)


rospy.init_node('sonar_node')

get_dis_front = rospy.Publisher('/car/give_me_front', String, queue_size=10)

get_dis_back = rospy.Publisher('/car/give_me_back', String, queue_size=10)
 
pub = rospy.Publisher("/car/chk_stop", String, queue_size=10)
 
rate=rospy.Rate(1)

def chk_front(fron):
	front_dist=fron.data	
	if front_dist < 15:
		pub.publish('stop')
        else:
                pub.publish('move')
	

front = rospy.Subscriber('/car/get_front', Int32, chk_front) 


while not rospy.is_shutdown():
	get_dis_front.publish("a")
	

	
	
