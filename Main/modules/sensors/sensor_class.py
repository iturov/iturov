#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Libraries
import RPi.GPIO as GPIO
import time
# Temperature Sensor
import TSYS01
# Pressure Sensor
import ms5837


class Sensor(object):
    def __init__(self):
        # Pin Configurations
        #self.trigPin = trigPin
        #self.echoPin = echoPin
        # Initializing Sensors
        self.init_pressure()
        #self.init_jst()
        self.temperature = 0
        self.freshwater_depth = 0
        self.pressure_mb = 0
        #self.distance = 0

    def init_pressure(self):
        try:
            self.pressure_sensor = ms5837.MS5837_30BA()
            self.pressure_sensor.init()
        except Exception:
            print("Pressure sensor could not be initialized")
            pass

    #def init_jst(self):
        # GPIO Mode (BOARD / BCM)
        #GPIO.setmode(GPIO.BCM)

# Set GPIO direction (IN / OUT)
        #GPIO.setup(self.trigPin, GPIO.OUT)
        #GPIO.setup(self.echoPin, GPIO.IN)

    def read_pressure(self):
        if self.pressure_sensor.read():
            try:    
                self.freshwater_depth = self.pressure_sensor.depth()
                self.pressure_mb = self.pressure_sensor.pressure()
                self.temperature = self.pressure_sensor.temperature()
            except:
                pass        
        else:
            print("Pressure sensor could not be read")
            self.freshwater_depth = "0"
            self.pressure_mb = "0"
            self.temperature = "0"

    def read_jst(self):
        try:
            GPIO.output(self.trigPin, True)
            time.sleep(0.00001)
            GPIO.output(self.trigPin, False)

            start_time = time.time()
            stop_time = time.time()

            while GPIO.input(self.echoPin) == 0:
                start_time = time.time()

            while GPIO.input(self.echoPin) == 1:
                stop_time = time.time()

            time_elapsed = stop_time - start_time

            self.distance = (time_elapsed * 34300) / 2
        except Exception:
            print("Ultrasonic sensor could not be read")

    def run(self):
        self.read_pressure()
        #self.read_jst()

    def debug(self):
        self.read_pressure()
        #self.read_jst()
        print("Pressure: %0.1f mbar\tDepth: %0.2f m\tTemp: %0.1f C") % (
            self.pressure_mb,
            self.freshwater_depth,
            self.temperature,
            self.distance)
