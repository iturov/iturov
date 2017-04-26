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

##- SERVO CONTROLLERS' PINS CONNECTED -## BEGIN
"PINS NUMBERS ARE GPIO PIN NUMBERS SEE: 'https://www.raspberrypi.org/documentation/usage/gpio/' "
servos = [24,23,4,17,27,22] #GPIO number
robotServos = [21,20,16]
#servos = [rightZ,leftZ,fowardLeft,fowardRight,backLeft,backRight] 
#robotServos = [elbow1,elbow2,gripper]
lightDriverPin = 12
##- SERVO CONTROLLERS' PINS CONNECTED -## END

##- MOTOR CONFIGURATION -##  
#---3-----4

#-1---------2

#---5-----6

##- GLOBAL DATAS
dataArray = [0,0,0,0,0,0,0,0,0]
servoDriver = pigpio.pi() 
escOffNonRev = 1100 #NON-REVERSABLE ESC'S STOP VALUE
escOffRev = 1750 #REVERSABLE ESC'S STOP VALUE
robotServoMax = 2000
robotServoMin = 600
##- GLOBAL DATAS

##- ARMING CONTROLLERS -## BEGIN
for i in range(0,200):
	##- ALL SERVO'S TO BE SET "0"
	##- FOR ARMING THE ESC'S BOTH REVERSABLE AND NON-REVERSABLE ESC'S SHOULD BE ARMED WITH 1000-1100 uS PULSE
    servoDriver.set_servo_pulsewidth(servos[0], escOffNonRev) 
    servoDriver.set_servo_pulsewidth(servos[1], escOffNonRev)
    servoDriver.set_servo_pulsewidth(servos[2], escOffNonRev)
    servoDriver.set_servo_pulsewidth(servos[3], escOffNonRev)
    servoDriver.set_servo_pulsewidth(servos[4], escOffNonRev)
    servoDriver.set_servo_pulsewidth(servos[5], escOffNonRev)
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
		

def execute_plugins():
    while 1:
		##- LIGHT DRIVER -## BEGIN
	    servoDriver.set_servo_pulsewidth(lightDriverPin, 1200 + int(dataArray[3]))
		##- LIGHT DRIVER -## END
        elbowValue = [int(dataArray[4]),int(dataArray[5]),int(dataArray[6])]
        for i in range(0,4):
            if elbowValue[i] < robotServoMin:
                elbowValue[i] = robotServoMin
            if elbowValue[i] > robotServoMax:
                elbowValue[i] = robotServoMax
            if elbowValue[i] == 0
                elbowValue[i] = 0
            servoDriver.set_servo_pulsewidth(robotServos[i],elbowValue[i])
        #servoDriver.set_servo_pulsewidth(robotServos[0],elbowValue[0])
        #servoDriver.set_servo_pulsewidth(robotServos[1],elbowValue[1])
        #servoDriver.set_servo_pulsewidth(robotServos[2],elbowValue[2])
        time.sleep(0.02)
        


##- pulsewidth can only set between 500-2500, SHOULDN'T cross the line!
def motors_write():
    while 1: #CREATE AN INFINITE LOOP
   		##- INCOMING DATA STRING TO INTEGER CONVERSION	-## BEGIN   
        dataArrayInt = [int(dataArray[0]),-int(dataArray[1]),int(dataArray[2]),int(dataArray[3]),int(dataArray[4]),int(dataArray[5]),int(dataArray[6]),int(dataArray[7]),int(dataArray[8])]
		##- INCOMING DATA STRING TO INTEGER CONVERSION	-## END
		#print dataArrayInt[7]
		##- Z AXIS ESC CONTROL -## BEGIN
        rollP = 0
        rollN = 0
        if dataArrayInt[7] > 0:
            rollP = dataArrayInt[7]
            rollN = 0
        if dataArrayInt[7] < 0:
            rollN = -dataArrayInt[7]
            rollP = 0
        if dataArrayInt[7] == 0:
            rollN = 0
            rollP = 0

        servoDriver.set_servo_pulsewidth(servos[0],escOffRev + dataArrayInt[0] + rollN)
        servoDriver.set_servo_pulsewidth(servos[1],escOffRev + dataArrayInt[0] + rollP)
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
    # messageBox.Show("Makine açılsın mı?"); :)
        yawP = 0
        yawN = 0
        if dataArrayInt[8] > 0:
            yawP = dataArrayInt[8]
            yawN = 0
        if dataArrayInt[8] < 0:
            yawN = -dataArrayInt[8]
            yawP = 0
	##- ANALYSING INCOMING DATA-## END
	
	    ##- Y AXIS ESC CONTROL (FOWARD/BACK)-## BEGIN
        servoDriver.set_servo_pulsewidth(servos[4],escOffNonRev + back + left + yawP)
        servoDriver.set_servo_pulsewidth(servos[5],escOffNonRev +  back + right + yawN)
	    ##- Y AXIS ESC CONTROL (FOWARD/BACK)-##
	
	    ##- X AXIS ESC CONTROL (RIGHT/LEFT)-## BEGIN
        servoDriver.set_servo_pulsewidth(servos[2],escOffNonRev + foward + left + yawN)
        servoDriver.set_servo_pulsewidth(servos[3],escOffNonRev + right + foward + yawP)
	    ##- X AXIS ESC CONTROL (BACK)-## END
        time.sleep(0.02)

def send_data():
    ##- SEND DATA TO SERVER
    while 1:
        time.sleep(0.1) ##- 
        send_data = str(random.randint(0,100)) ##- SENDING RANDOM VALUES TO SERVER, THIS WILL BE CHANGED TO SENSOR VALUES!
        print "sending data..." + send_data + "\n"
        client_socket.send(send_data + "\n")



if __name__ == "__main__":

    print "*******TCP/IP ITUROV COMMUNICATION PROGRAM********"
    print "Connecting to server at 192.168.137.1:8092"
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.137.1', 8092)) # CONNECTING TO LOCALLY CONNECTED SERVER ON PORT 8092. 
    	##- ON PORT 8091 CAMERA IS STREAMED
    print "Connected to server at 192.168.137.1:8092"
	
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

