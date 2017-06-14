import socket
import thread
import sys
import time
import random

from modules.sensors.sensor_class import *
from modules.sensors.serial_class import *

sensor = Sensor()
serial_node = SerialNode()
send_data = "0,0,0,0"
dataArray = []
array = []
client_socket = None
arduino_data = "0"
servo_values = [0, 0, 0, 0, 0]
data_sending = "0,0,0,0,0"

def initialize(_ip = '192.168.137.1',_port = 8092):
    global client_socket
    port = _port
    ip = _ip
    print "ITU ROV CLIENT PROGRAM STARTED"
    print "CONNECTING TO SERVER AT" + ip + ":" + str(port)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port)) # CONNECTING TO LOCALLY CONNECTED SERVER ON PORT 8092.

def establish():
    thread.start_new_thread(_get_sensors,())
    thread.start_new_thread(_recv_data,())
    thread.start_new_thread(_send_data,())
    thread.start_new_thread(_get_arduino,())
    thread.start_new_thread(_run_servo, ())

def _get_arduino():
    while 1:
        global serial_node
        global arduino_data
        global servo_values
        serial_node.read_data()
        arduino_data = str(serial_node.msg)
        
def _run_servo():
    while 1:
        global servo_values
        global dataArray
        global data_sending
        global serial_node

        servo_values[0] = dataArray[5]
        servo_values[1] = dataArray[6]
        servo_values[2] = dataArray[7]
        servo_values[3] = dataArray[8]
        servo_values[4] = dataArray[9]
        data_sending = (str(servo_values[0]) + "," + str(servo_values[1]) + "," + str(servo_values[2]) + "," + str(servo_values[3]) + "," + str(servo_values[4]))
#        data_sending = "hello"
        serial_node.write_data(data_sending + "\n")

def _get_sensors():
    while 1:
        global sensor
        global serial_node
        global send_data
        global arduino_data

        pressure = "0"
        temp_normal = "0"
        depth = "0"

        sensor.read_pressure()
        pressure = str(sensor.pressure_mb)
        depth = str(sensor.freshwater_depth)
        temp_normal = str(sensor.temperature)

        send_data = pressure + "," + depth + "," + temp_normal + "," + arduino_data

def _send_data():
    i = 0
    ##- SEND DATA TO SERVER
    while 0:
        global client_socket
        #time.sleep(0.01) ##-
        #send_data = (pressure + "," + depth + "," + temp_normal + "," + dist + "," + arduino$
        send_data = "12,12,12,12,12,23," + str(i)
        #print "sending data..." + send_data + "\n"
        client_socket.send(send_data + "\n")
        i += 1

    while 1:
        global client_socket
        global send_data
        try:        
#            print "Data Sending: " + send_data + "\n"
            client_socket.send(send_data + "\n")
        except:
            pass



def _recv_data():
    while True:
        global client_socket
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
            global dataArray
            global array
            array = recv_data.split(",")
            for i in range(0,len(array)):
                if array[i] == "": # search for nulls
                    array[i] = "0" # replace nulls with "0"
                #dataArray[i] = int(array[i])
                #dataArray = array
            try:
                dataArray = [int(x) for x in array]
            except:
                pass
            #print dataArray

def kill():
    global client_socket
    client_socket.close()
