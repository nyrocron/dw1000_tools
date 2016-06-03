#!/usr/bin/env python3

# Copyright (c) 2016 Florian Tautz <dev@nyronet.de>

import socket
from sys import argv, stdout, stderr

addr = (argv[1], int(argv[2]))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(addr)

while True:
    try:
        data, addr = sock.recvfrom(1000)
        stdout.buffer.write(data)
    except KeyboardInterrupt:
        print("Keyboard interrupt", file=stderr)
        break

