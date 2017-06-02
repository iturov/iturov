import time
import sys
import thread
#sys.path.append("/modules/motorController")
#sys.path.append("/modules/network")

from modules.network import network
from modules.motorControllers import controller

_network = network
_motor_controller = controller
motor_pins = [17,18,27,25,16,21]
servo_off_value = 1450
incoming_data = []


def _variable_control():
    while True:
        incoming_data = _network.dataArray
        _motor_controller.arrayInt = incoming_data
        print incoming_data

if True:
    thread.start_new_thread(_variable_control,())
    _network.initialize('192.168.137.1')
    _network.establish()

#    time.sleep(1)
    _motor_controller.initialize(motor_pins,servo_off_value)
#    time.sleep(1)
    _motor_controller.run()
    print "Run"

    try:
        while 1:
            continue
    except:
        print "Client program quits...."
_network.kill()
