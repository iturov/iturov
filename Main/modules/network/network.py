import socket
import thread
import sys
import time

dataArray = []
array = []
client_socket = None

def initialize(_ip = '192.168.137.1',_port = 8092):
    global client_socket
    port = _port
    ip = _ip
    print "ITU ROV CLIENT PROGRAM STARTED"
    print "CONNECTING TO SERVER AT" + ip + ":" + str(port)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port)) # CONNECTING TO LOCALLY CONNECTED SERVER ON PORT 8092.

def establish():
    thread.start_new_thread(_recv_data,())
    thread.start_new_thread(_send_data,())

def _send_data():
    ##- SEND DATA TO SERVER
    while True:
        global client_socket
        time.sleep(0.1) ##-
        #send_data = (pressure + "," + depth + "," + temp_normal + "," + dist + "," + arduino_data)
        send_data = "sending data 123"
        #print "sending data..." + send_data + "\n"
        client_socket.send(send_data + "\n")

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
            dataArray = [int(x) for x in array]
            #print dataArray

def kill():
    global client_socket
    client_socket.close()
