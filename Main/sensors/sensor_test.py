#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sensor_class import *
import time

def main():
    sensor = Sensor(19, 26)
    #sensor.debug()
    while True:
        sensor.read_jst()
        sensor.read_pressure()
        dist = sensor.distance
        temperature = sensor.temperature
        pressure = sensor.pressure_mb
        depth = sensor.freshwater_depth
        print("Distance: %0.1f cm\t Temp: %0.2f C\tPressure:  %0.1f mbar") % (dist, temperature, pressure)


if __name__ == "__main__":
    main()
