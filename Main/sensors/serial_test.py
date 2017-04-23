#!/usr/bin/env python
# -*- coding: utf-8 -*-

from serial_class import *
import time

serial_node = SerialNode()

while True:
    serial_node.read_data()
    print(serial_node.msg)
    time.sleep(0.1)
