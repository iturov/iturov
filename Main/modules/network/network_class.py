import socket
import thread
import sys
import time
from ..sensors.sensor_class import *
from ..sensors.serial_class import *

class Connection():
    dataArray = []

    def __init__(self, trig, echo):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('192.168.137.1', 8092)) # CONNECTING TO LOCALLY CONNECTED SERVER ON PORT 8092.
        self.trig = trig
        self.echo = echo
        self.sensor = Sensor(self.trig, self.echo)
        self.serial_node = SerialNode()


    def establish(self):
        thread.start_new_thread(Connection.recv_data,())
        thread.start_new_thread(Connection.send_data,())

    def send_data():
        ##- SEND DATA TO SERVER
        while True:
            time.sleep(0.1) ##-
            self.sensor.read_pressure()
            self.pressure = str(self.sensor.pressure_mb)
            self.depth = str(self.sensor.freshwater_depth)
            self.temp_normal = str(self.sensor.temperature)
            self.dist = str(self.sensor.distance)
            # TEMPERATURE AND BLUETOOTH DATA
            self.serial_node.read_data()
            self.arduino_data = str(self.serial_node.msg)
            self.send_data = (self.pressure + "," + self.depth + "," + self.temp_normal + "," + self.dist + "," + self.arduino_data)

            print "sending data..." + self.send_data + "\n"
            self.client_socket.send(self.send_data + "\n")

    def recv_data(self):
        while True:
            try:
    		    self.recv_data = client_socket.recv(1024)
            except:
                #Handle the case when server process terminates
    		    print "Server closed connection, thread exiting."
    		    thread.interrupt_main()
    		    break
            if not self.recv_data:
                # Recv with no data, server closed connection
                print "Server closed connection, thread exiting."
                thread.interrupt_main()
                break
            else:
                dataArray = self.recv_data.split(",")
                for i in range(0,len(dataArray))

                    if dataArray[i] == "" # search for nulls
                        dataArray[i] = "0" # replace nulls with "0"
