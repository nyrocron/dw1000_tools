#!/bin/sh

# dev environment setup script
# this just pulls the required things for compiling the kernel module from github

git clone --depth=1 git://github.com/raspberrypi/tools

git clone --depth=1 -b rpi-4.4.y git://github.com/raspberrypi/linux linux-4.4
ln -s linux-4.4 linux

git clone https://github.com/nyrocron/dw1000

