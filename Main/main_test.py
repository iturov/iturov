import time
import sys
import thread

from modules.network import network
from modules.motorControllers import controller
from modules.roboticArmController import robot_controller

_network = network
_motor_controller = controller
_robot_controller = robot_controller
motor_pins = [17,18,27,25,16,21]
servo_off_value = 1450
incoming_data = []


def _variable_control():
    while True:
        incoming_data = _network.dataArray
        _motor_controller.arrayInt = incoming_data
        _robot_controller.array = incoming_data
        if incoming_data:
            for i in range(0, 5):
                _robot_controller.servo_values[i] = int(incoming_data[i + 1]) # NOTE: "3" WILL BE CHANGED TO THE POSITION WHERE ROBOT DATA BEGINS 
        print incoming_data
        print _network.send_data
        time.sleep(0.1)

if True:
    thread.start_new_thread(_variable_control,())
    _network.initialize('192.168.2.105')
    _network.establish()

    _motor_controller.initialize(motor_pins,servo_off_value)
    _robot_controller.initialize()
    _motor_controller.run()
    _robot_controller.run()
    print "Run"

    try:
        while 1:
            continue
    except:
        print "Client program quits...."
_network.kill()
