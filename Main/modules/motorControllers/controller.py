import pigpio
import time
import thread
from ..network import network_class

class Motors(object):

    def __init__(self,pins = [], servo_off_value = 1500):
        self.pins = pins
        self.servoOffValue = servoOffValue
        self.servo_driver = pigpio.pi()


    def attach(self):
        for i in range(0,100):
        	servo_driver.set_servo_pulsewidth(self.pins[0], self.servo_off_value)
        	servo_driver.set_servo_pulsewidth(self.pins[1], self.servo_off_value)
        	servo_driver.set_servo_pulsewidth(self.pins[2], self.servo_off_value)
        	servo_driver.set_servo_pulsewidth(self.pins[3], self.servo_off_value)
        	servo_driver.set_servo_pulsewidth(self.pins[4], self.servo_off_value)
        	servo_driver.set_servo_pulsewidth(self.pins[5], self.servo_off_value)
        	time.sleep(0.02)

    def run(self):
        thread.start_new_thread(_run_thread,())

    def _run_thread(self):
        #DECLERATION
        self.motors = []
        self.arrayInt = []

        while True: # Create a loop
            for i in range(0,len(Connection.dataArray)) # for each i in range 0-lenght of dataArray's array
                self.arrayInt[i] = int(Connection.dataArray[i]) # convert datas to integer

            # data conversion
            self.throttle = self.arrayInt[2]
            self.fowardBack = self.arrayInt[0]
            self.leftRight = self.arrayInt[1]
            self.roll = self.arrayInt[3]
            self.yaw = self.arrayInt[4]

            # Z-axis
            self.motors[0] = (-self.throttle) + (-self.roll) # motor1
            self.motors[1] = (-self.throttle) + (self.roll) # motor2
            # XY-plane
            self.motors[2] = (-self.fowardBack) + (-self.leftRight) + (-self.yaw) # motor3
            self.motors[3] = (-self.fowardBack) + (self.leftRight) + (self.yaw) # motor4
            self.motors[4] = (self.fowardBack) + (-self.leftRight) + (self.yaw) # motor5
            self.motors[5] = (self.fowardBack) + (self.leftRight) + (-self.yaw) # motor6
            for i in range(0,6):
                self.motors[i] = constrain(self.motors[i], 0, 1000)
                self.servo_driver.set_servo_pulsewidth(self.pins[i], 1000 + self.motors[i])
                time.sleep(0.02)

    def constrain(self, value, min = 0, max = 1000):
        if self.value > self.max:
            self.value = self.max
        if self.value < self.min:
            self.value = self.min
        return(self.value)
