# NOTE: BeeROV motor controller algoritm/structure. functions starting with "_" underscore are private functions that user does NOT call.

import pigpio
import time
import thread
import pid

# NOTE: PID's should be enabled, see function "run"
depth_pid = pid
roll_pid = pid

# NOTE: in this algoritm a reversible motor library is created, uses 1500 us as an off VALUE
servo_off_value = 1500
depth_feedback = 0
roll_feedback
servo_driver = pigpio.pi()
arrayInt = [0,0,0,0,0,0,0,0,0,0,0,0,0]
pins = [0,0,0,0,0,0]

def initialize(_pins = [1,2,3,4,5,6], _servo_off_value = 1500):
    global pins
    global servo_off_value
    servo_off_value = _servo_off_value
    pins = _pins
    for k in range(0,50):
        for i in range(0,len(pins)):
            servo_driver.set_servo_pulsewidth(pins[i], servo_off_value)
        time.sleep(0.02)

def _run_thread():
    motors = [0,0,0,0,0,0]
    while 1:
        global arrayInt
        global pins
        #conversion
        throttle = arrayInt[0]
        fowardBack = arrayInt[1]
        leftRight = arrayInt[2]
        roll = arrayInt[7]
        yaw = arrayInt[8]
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
            motors[i] = _constrain(motors[i], -500, 500)
            servo_driver.set_servo_pulsewidth(pins[i], servo_off_value + motors[i])
        print motors
        time.sleep(0.02)

def run(pid_state = 0): # NOTE: set pid_state to 1 to enable pid controller
    if pid_state == 0:
        thread.start_new_thread(_run_thread,()) # NOTE: start without a pid controller
    if pid_state == 1:
        thread.start_new_thread(_run_with_pid,()) # NOTE: start with a pid controller

def _run_with_pid():
    motors = [0,0,0,0,0,0]
    while 1:
        global arrayInt
        global pins
        #conversion
        z_speed = arrayInt[0]
        fowardBack = arrayInt[1]
        leftRight = arrayInt[2]
        roll_speed = arrayInt[7]
        yaw = arrayInt[8]
        throttle = depth_pid.calculate(z_speed, depth_feedback, 1, 1, 1, 1) # NOTE: feedback values are coming from sensor depth sensor
        roll = roll_pid.calculate(roll_speed, roll_feedback, 1, 1, 1, 1) # NOTE: feedback2 value comes from the IMU sensor
        motors[0] = throttle + roll # NOTE: multiply roll with -1 if correction is wrong
        motors[1] = throttle - roll
        # XY-plane
        motors[2] = (-fowardBack) + (-leftRight) + (-yaw) # motor3
        motors[3] = (-fowardBack) + (leftRight) + (yaw) # motor4
        motors[4] = (fowardBack) + (-leftRight) + (yaw) # motor5
        motors[5] = (fowardBack) + (leftRight) + (-yaw) # motor6
        #conversion
        # NOTE: the rest of the motors on the XY plane are non-pid controlled motors, will be added in the future
        for i in range(2,len(pins)):
            motors[i] = _constrain(motors[i], -500, 500)
            servo_driver.set_servo_pulsewidth(pins[i], servo_off_value + motors[i])
        print motors
        time.sleep(0.02)

def _constrain(value, min = 0, max = 1000):
    if value > max:
        value = max
    if value < min:
        value = min
    return(value)
