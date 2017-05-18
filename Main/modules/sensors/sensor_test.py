#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sensor_class import *
import time

def main():
    sensor = Sensor(19, 26)
    while True:
        sensor.debug()

if __name__ == "__main__":
    main()
