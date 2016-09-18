#!/bin/bash
wget abyz.co.uk/rpi/pigpio/pigpio.zip
unzip pigpio.zip
cd PIGPIO
make -j4
sudo make install

sudo pip install tornado

sudo mv controlgeek/pigpiod.service /etc/systemd/system
sudo mv controlgeek/controlgeek.service /etc/systemd/system

sudo systemctl enable pigpiod.service
sudo systmectl enable controlgeek.service
