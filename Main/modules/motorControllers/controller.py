import pigpio
import time
import thread

servo_off_value = 1500
servo_driver = pigpio.pi()
arrayInt = []
pins = []

def initialize(_pins = [1,2,3,4,5,6], _servo_off_value = 1500):
    global pins
    global servo_off_value
    servo_off_value = _servo_off_value
    pins = _pins
    for k in range(0,100):
        for i in range(0,len(pins)):
            servo_driver.set_servo_pulsewidth(pins[i], servo_off_value)
        time.sleep(0.02)

def _run_thread():
    motors = []
    while 1:
        global arrayInt
        global pins
        #conversion
        throttle = arrayInt[2]
        fowardBack = arrayInt[0]
        leftRight = arrayInt[1]
        roll = arrayInt[3]
        yaw = arrayInt[4]
        # Z-axis
        motors[0] = (-throttle) + (-roll) # motor1
        motors[1] = (-throttle) + (roll) # motor2
        # XY-plane
        motors[2] = (-fowardBack) + (-leftRight) + (-yaw) # motor3
        motors[3] = (-fowardBack) + (leftRight) + (yaw) # motor4
        motors[4] = (fowardBack) + (-leftRight) + (yaw) # motor5
        motors[5] = (fowardBack) + (leftRight) + (-yaw) # motor6
        #conversion
        for i in range(0,len(pins)):
            motors[i] = _constrain(motors[i], 0, 1000)
            servo_driver.set_servo_pulsewidth(pins[i], 1000 + motors[i])
        time.sleep(0.02)

def run():
    thread.start_new_thread(_run_thread,())

def _constrain(self, value, min = 0, max = 1000):
    if value > max:
        value = max
    if value < min:
        value = min
    return(value)
