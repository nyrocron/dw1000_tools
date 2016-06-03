#!/usr/bin/env python3

# Copyright (c) 2016 Florian Tautz <dev@nyronet.de>

import socket
from sys import argv, stdin
from time import sleep

MTU = 1000 - 9 - 24 - 8
delay = float(argv[3])

addr = (argv[1], int(argv[2]))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    chunk = stdin.buffer.read(MTU)
    sock.sendto(chunk, addr)
    if len(chunk) < MTU:
        break
    sleep(delay)

