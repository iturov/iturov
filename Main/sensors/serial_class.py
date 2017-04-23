#!/usr/bin/env python
# -*- coding: utf-8 -*-

from glob import glob
import serial

class SerialNode(object):
    def __init__(self):
        self.ports = glob('/dev/ttyUSB*')
        self.serials = []
        self.msg = 0
        self.add_serials()
        
    def add_serials(self):
        print("*** Adding serials...")
        for port in self.ports:
            try:
                self.serials.append(serial.Serial(port, 115200))
            except Exception as e:
                print e

    def read_data(self):
        if self.serials:
            if self.serials[0].inWaiting:
                self.serials[0].flush()
                try:
                    self.msg = self.serials[0].readline().split("\r\n")
                except Exception:
            	    print("Cannot read messages from serial")
                    pass          
