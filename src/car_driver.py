#!/usr/bin/env python



import rospy
#from std_msgs.msg import Bool
from std_msgs.msg import Int32
from std_msgs.msg import String
#from robot.msg import sonar
import serial

distpub = rospy.Publisher('/car/move', String, queue_size=10)
get_front=rospy.Publisher('/car/get_front',Int32, queue_size=10)
get_back=rospy.Publisher('/car/get_back',Int32, queue_size=10)

ser=serial.Serial()

stop=False

def init():
     rospy.init_node('car_node')
     rospy.Subscriber("/act/car/send_move_command", String, callback_move)
     rospy.Subscriber("/car/give_me_front",String,callback_front)     
     rospy.Subscriber("/car/chk_stop", String, callback_stop)    
     ser.baudrate=9600
     ser.port='/dev/rfcomm2'
     ser.timeout=2
     ser.open()
     if not(ser.isOpen()):
         rospy.logerr("Error: Could not open bluetooth Serial Port")


def serial_write(strng):
    try:
        ser.write(strng)
    except:
        if (ser.isOpen()):ser.close()
        if not(ser.isOpen()):ser.open()
        rospy.logerr("Error writing to serial port")

def callback_front(distance):
	serial_write(distance.data)

def callback_stop(inpu):
        global stop
	if inpu.data == "stop":    
              stop=True	
	      serial_write('f')	      
        elif inpu.data =="move":
              stop=False
	      serial_write('d')
	print inpu.data,stop

def callback_move(move):	
    sig=move.data
    global stop
    if not stop:
    	if (sig=="w"):
   		distpub.publish("Forward")
      		serial_write('d')
	elif (sig=="a"):
   		distpub.publish("Left")
      		serial_write('h')
	elif (sig=="s"):
   		distpub.publish("Stop")
      		serial_write('f')
	elif (sig=="d"):
   		distpub.publish("Right")
      		serial_write('g')
    
	



def parse(txt):
	get_front.publish(eval(txt))


def poll():
    rate=rospy.Rate(10)
    while not rospy.is_shutdown():
        try:
            parse(ser.readline())            
        except:
            if(ser.isOpen()):ser.close()
            if not(ser.isOpen()):ser.open()
            if not(ser.isOpen()): rospy.logerr("could not open bluetooth serial port")
        rate.sleep()

if __name__=='__main__':
    init()
    poll()

