#!/bin/bash
export HISTIGNORE='*sudo -S*'
echo "raspberry" | sudo -S pigpiod
cd ~/ROV/iturov/Main/sensors
python vehicleTestCode.py
cd ~/ROV/iturov
./streamer.sh