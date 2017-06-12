import time
import thread
from modules.sensors.serial_class import *

serial_node = SerialNode()
servo_default_position = [1520, 1520, 1520, 1520, 1520] #uS
servo_values = [0, 0, 0, 0, 0]

def initialize(_servo_default_position = [1520, 1520, 1520, 1520, 1520]):
    global servo_defaut_position
    servo_default_position = _servo_default_position
    global serial_node
    serial_node.write_data(str(servo_default_position[0]) + "," + str(servo_default_position[1]) + "," + str(servo_default_position[2]) + "," + str(servo_default_position[3]) + "," + str(servo_default_position[4]))

def run():
    thread.start_new_thread(_run_servo, ())

def _run_servo():
    while True:
        global servo_values
        global serial_node
        if serial_node:
            serial_node.write_data(str(servo_values[0]) + "," + str(servo_values[1]) + "," + str(servo_values[2]) + "," + str(servo_values[3]) + "," + str(servo_values[4]))
