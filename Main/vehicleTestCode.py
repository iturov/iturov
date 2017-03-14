# The client program connects to server and sends data to other 
# connected clients through the server
import pigpio
import socket
import thread
import sys
import time
import random
import datetime

servos = [24,23,4,17,27,22] #GPIO number
#####---- MOTOR CONFIGURATION ----#####
###3#####4

#1#########2

###5#####6
dataArray = [0,0,0,0,0,0,0]
servoDriver = pigpio.pi()

for i in range(0,200):
	servoDriver.set_servo_pulsewidth(servos[0], 1000)
	servoDriver.set_servo_pulsewidth(servos[1], 1000)
	servoDriver.set_servo_pulsewidth(servos[2], 1000)
	servoDriver.set_servo_pulsewidth(servos[3], 1000)
	servoDriver.set_servo_pulsewidth(servos[4], 1000)
	servoDriver.set_servo_pulsewidth(servos[5], 1000)
	time.sleep(0.02)

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


#dataArray[0] = throttle
#dataArray[1] = foward/back
#dataArray[2] = right/left
#dataArray[3] = - not set
#dataArray[4] = - not set
#dataArray[5] = - not set
#dataArray[6] = - not set
#...
#..
#.



#pulsewidth can only set between 500-2500

#try:
def motors_write():
   while 1:
        ######-- Z AXIS ESC CONTROL --######
        #print dataArray
	dataArrayInt = [int(dataArray[0]),int(dataArray[1]),int(dataArray[2]),0,0,0]
	if(dataArrayInt[0] > 10):
		dataArrayInt[0] += 500
	if(dataArrayInt[0] < -10):
		dataArrayInt[0] *= -1
	if(dataArrayInt[0] == 3):
		dataArrayInt[0] = 500
	servoDriver.set_servo_pulsewidth(servos[0],1000 + dataArrayInt[0])
        print("Servo {} {} micro pulses".format(servos, dataArray[0]))
        servoDriver.set_servo_pulsewidth(servos[1],1000 + dataArrayInt[0])
        print("Servo {} {} micro pulses".format(servos, dataArray[0]))
        ######-- Z AXIS ESC CONTROL --######
	dataArray[1] = 0
	dataArray[2] = 0
        if(dataArray[1] > 0):
            	foward = dataArray[1]
            	back = 0
        if(dataArray[1] < 0):
            	foward = 0
            	back = -dataArray[1]
        if(dataArray[2] > 0):
           	right = dataArray[2]
            	left = 0
        if(dataArray[2] < 0):
            	right = 0
            	left = -dataArray[2]
	if(dataArray[1] == 0):
		foward = 0
		back = 0
	if(dataArray[2] == 0):
		right = 0
		left = 0
	back=0
	foward=0
	back=0  
	left=0 
        ######-- Y AXIS ESC CONTROL (FOWARD/BACK)--######
        servoDriver.set_servo_pulsewidth(servos[4],1000 + int(back) + int(left))
        print("Servo {} {} micro pulses".format(servos,  int(back) + int(left)))
        servoDriver.set_servo_pulsewidth(servos[5],1000 +  int(back) + int(right))
        print("Servo {} {} micro pulses".format(servos, int(back) + int(right)))
        ######-- Y AXIS ESC CONTROL (FOWARD/BACK)--######

        ######-- X AXIS ESC CONTROL (RIGHT/LEFT)--######
        servoDriver.set_servo_pulsewidth(servos[2],1000 + int(foward) + int(left))
        print("Servo {} {} micro pulses".format(servos,  int(foward) + int(left)))
        servoDriver.set_servo_pulsewidth(servos[3],1000 + int(right) + int(foward))
        print("Servo {} {} micro pulses".format(servos, int(foward) + int(right)))
        ######-- X AXIS ESC CONTROL (BACK)--######
	#thread.interrupt_main()        


        time.sleep(0.02)
   # switch all servos off
#except KeyboardInterrupt:
#    for s in servos:
 
#        servoDriver.set_servo_pulsewidth(s, 0);
 
#servoDriver.stop()

def send_data():
    #! sleep(0.05)
    "Send data from other clients connected to server"
    while 1:
        time.sleep(0.1)
        #sleep( random.randint( 1, 6 ) )
        #send_data = str(raw_input("Enter data to send (q or Q to quit):"))
        #send_data = str(datetime.datetime.now())
        send_data = str(random.randint(0,100))
        print "sending data..." + send_data + "\n"
        if send_data == "q" or send_data == "Q":
            client_socket.send(send_data)
            thread.interrupt_main()
            break
        else:
            client_socket.send(send_data + "\n")

if __name__ == "__main__":

    print "*******TCP/IP Chat client program********"
    print "Connecting to server at 192.168.1.100:11000"

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.1.100', 11000))
    #host =  '192.168.1.102'
    #port = 11000
    #client_socket.connect(host, port)
    print "Connected to server at 192.168.1.100:11000"

    thread.start_new_thread(recv_data,())
    thread.start_new_thread(send_data,())
    thread.start_new_thread(motors_write,())
    try:
        while 1:
            continue
    except:
        print "Client program quits...."
client_socket.close()

