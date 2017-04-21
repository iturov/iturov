#!/usr/bin/env python
# -*- coding: utf-8 -*-

import TSYS01

sensor=TSYS01.TSYS01(0x77)
while True:
    print 'Temperature = %3.3f C' % sensor.readTemp()
