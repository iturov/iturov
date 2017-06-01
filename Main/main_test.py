import sys
import thread
sys.path.append("/modules/motorController")
sys.path.append("/modules/network")

import controller as motor_controller
import network as _network

motor_pins = []
servo_off_value = 0
incoming_data = []


def variable_control():
    while True:
        incoming_data = _network.dataArray
        motor_controller.arrayInt = incoming_data

if True:
    thread.start_new_thread(variable_control,())
    _network.initialize()
    _network.establish()
    motor_controller.initialize(motor_pins,servo_off_value)
    motor_controller.run()


    try:
        while 1:
            continue
    except:
        print "Client program quits...."
_network.kill()
