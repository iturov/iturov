##-ROV RASPBERRY PI'S SIDE CONTROL PROGRAM
##-THIS PROGRAM COMMUNICATES TO GROUND CONTROL STATION DIRECT CONNECTED TO THE RASPBERRY, 
##-EXECUTES MOVEMENT ALGORITHMS WITH RECEIVED DATA,
##-CONTROLS ADDITIONAL PLUGINS WITH RECEIVED DATA
##-SENDS FEEDBACK, SENSOR VALUES BACK TO GROUND CONTROL STATION

##-FOR FURTHER SUPPORT VISIT: "www.github.com/iturov"
##-THIS PROGRAM IS CURRENTLY UNDER DEVELOPMENT BY ISTANBUL TECHNICAL UNIVERSITY ROV TEAM

import pigpio
import socket
import thread
import sys
import time
import random
import datetime
from sensor_class import *
from serial_class import *

##- SERVO CONTROLLERS' PINS CONNECTED -## BEGIN
"PINS NUMBERS ARE GPIO PIN NUMBERS SEE: 'https://www.raspberrypi.org/documentation/usage/gpio/' "
servos = [24,23,4,17,27,22] #GPIO number
lightDriverPin = 20
##- SERVO CONTROLLERS' PINS CONNECTED -## END

##- MOTOR CONFIGURATION -##  
#---3-----4

#-1---------2

#---5-----6

##- GLOBAL DATAS
dataArray = [0,0,0,0,0,0,0]
servoDriver = pigpio.pi() 
escOffNonRev = 1100 #NON-REVERSABLE ESC'S STOP VALUE
escOffRev = 1750 #REVERSABLE ESC'S STOP VALUE
##- GLOBAL DATAS

##- ARMING CONTROLLERS -## BEGIN
for i in range(0,200):
	##- ALL SERVO'S TO BE SET "0"
	##- FOR ARMING THE ESC'S BOTH REVERSABLE AND NON-REVERSABLE ESC'S SHOULD BE ARMED WITH 1000-1100 uS PULSE
	servoDriver.set_servo_pulsewidth(servos[0], escOffRev) 
	servoDriver.set_servo_pulsewidth(servos[1], escOffRev)
	servoDriver.set_servo_pulsewidth(servos[2], escOffRev)
	servoDriver.set_servo_pulsewidth(servos[3], escOffRev)
	servoDriver.set_servo_pulsewidth(servos[4], escOffRev)
	servoDriver.set_servo_pulsewidth(servos[5], escOffRev)
	time.sleep(0.02)
##- ARMING CONTROLLERS -## END

##- INCOMING DATA DETAILS
#dataArray[0] = throttle
#dataArray[1] = foward/back
#dataArray[2] = right/left
#dataArray[3] = light value (0 - 700)
#dataArray[4] = - not set
#dataArray[5] = - not set
#dataArray[6] = - not set
#...
#..
#.

def recv_data():
    "Receive data from other clients connected to server"
    while 1:
        try:
            recv_data = client_socket.recv(1024)
        except:
            #Handle the case when server process terminates
            print "Server closed connection, thread exiting."
            thread.interrupt_main()
            break
        if not recv_data:
                # Recv with no data, server closed connection
                print "Server closed connection, thread exiting."
                thread.interrupt_main()
                break
        else:
                #print "Received data: ", recv_data
                global dataArray
                dataArray = recv_data.split(",")
		print dataArray[0]
		print dataArray[3]




def execute_plugins():
	##- LIGHT DRIVER -## BEGIN
	servoDriver.set_servo_pulsewidth(lightDriverPin, 1200 + int(dataArray[3]))
	##- LIGHT DRIVER -## END



##- pulsewidth can only set between 500-2500, SHOULDN'T cross the line!
def motors_write():
   	while 1: #CREATE AN INFINITE LOOP
    ##- INCOMING DATA STRING TO INTEGER CONVERSION	-## BEGIN   
		dataArrayInt = [int(dataArray[0]),int(dataArray[1]),int(dataArray[2]),int(dataArray[3]),int(dataArray[4]),int(dataArray[5]),int(dataArray[6])]
	##- INCOMING DATA STRING TO INTEGER CONVERSION	-## END

	##- Z AXIS ESC CONTROL -## BEGIN
		servoDriver.set_servo_pulsewidth(servos[0],escOffRev + dataArrayInt[0])
    		servoDriver.set_servo_pulsewidth(servos[1],escOffRev + dataArrayInt[0])
    ##- Z AXIS ESC CONTROL -## END
	
	##- ANALYSING INCOMING DATA-## BEGIN

	##--##- DECLERATION OF AXIS/DIRECTION VALUES -## BEGIN
		foward = 0
		back = 0
		right = 0
		left = 0
	##--##- DECLERATION OF AXIS/DIRECTION VALUES-## END

		if(dataArrayInt[1] > 0):
       			foward = dataArrayInt[1]
       			back = 0
    		if(dataArrayInt[1] < 0):
       			foward = 0
       			back = -dataArrayInt[1]
    		if(dataArrayInt[2] > 0):
       			right = dataArrayInt[2]
        		left = 0
    		if(dataArrayInt[2] < 0):
        		right = 0
        		left = -dataArrayInt[2]
	
		if(dataArrayInt[1] == 0):
			foward = 0
			back = 0
		if(dataArrayInt[2] == 0):
			right = 0
			left = 0
		##- ANALYSING INCOMING DATA-## END

    ##- Y AXIS ESC CONTROL (FOWARD/BACK)-## BEGIN
    		servoDriver.set_servo_pulsewidth(servos[4],escOffNonRev + back + left)
    		servoDriver.set_servo_pulsewidth(servos[5],escOffNonRev +  back + right)
    ##- Y AXIS ESC CONTROL (FOWARD/BACK)-##

    ##- X AXIS ESC CONTROL (RIGHT/LEFT)-## BEGIN
    		servoDriver.set_servo_pulsewidth(servos[2],escOffNonRev + foward + left)
    		servoDriver.set_servo_pulsewidth(servos[3],escOffNonRev + right + foward)
    ##- X AXIS ESC CONTROL (BACK)-## END
		time.sleep(0.02)

def send_data():
    ##- SEND DATA TO SERVER
    while 1:
        time.sleep(0.1) ##-
        sensor.run()
        pressure = str(sensor.pressure_mb)
        depth = str(sensor.freshwater_depth)
        temp_normal = str(sensor.temperature)
        dist = str(sensor.distance)
        # TEMPERATURE AND BLUETOOTH DATA
        serial_node.read_data()
        arduino_data = str(serial_node.msg)
        send_data = (pressure + "," + depth + "," + temp_normal + "," + dist + "," + arduino_data) 
        print "sending data..." + send_data + "\n"
        if send_data == "q" or send_data == "Q":
            client_socket.send(send_data)
            thread.interrupt_main()
            break
        else:
            client_socket.send(send_data + "\n")



if __name__ == "__main__":

    print "*******TCP/IP ITUROV COMMUNICATION PROGRAM********"
    print "Connecting to server at 192.168.137.1:8092"
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.137.1', 8092)) # CONNECTING TO LOCALLY CONNECTED SERVER ON PORT 8092. 
    ##- ON PORT 8091 CAMERA IS STREAMED
    print "Connected to server at 192.168.137.1:8092"

    # Initialize sensors, echo sounder's trig pin to gpio 19 and echo pin to 26
    sensor = Sensor(19, 26)
    serial_node = SerialNode()

    ##- BEGIN THREADING FUNCTIONS SIMULTANEOUSLY -## BEGIN
    thread.start_new_thread(recv_data,()) #RECEIVING DATA FROM THE SERVER
    thread.start_new_thread(send_data,()) #SENDING DATA BACK TO SERVER
    thread.start_new_thread(motors_write,()) #EXECUTING MOTOR CONTROL ALGORITHM
    thread.start_new_thread(execute_plugins,()) #EXECUTE ADDITIONAL PLUGINS
    ##- BEGIN THREADING FUNCTIONS SIMULTANEOUSLY -## END

    try:
        while 1:
            continue
    except:
        print "Client program quits...."
client_socket.close()

