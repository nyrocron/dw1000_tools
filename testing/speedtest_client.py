#!/usr/bin/env python3

# Copyright (c) 2016 Florian Tautz <dev@nyronet.de>

import socket
from sys import argv, stdin
from time import sleep
from datetime import datetime, timedelta
import json

MTU = 950
delay = float(argv[3])
npackets = int(argv[4])

if len(argv) > 5 and argv[5].isnumeric():
    MTU = int(argv[5])

addr = (argv[1], int(argv[2]))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

packet_counter = 0
bytes_counter = 0
with open('/dev/urandom', 'rb') as infh:
    start = datetime.now()
    for i in range(npackets):
        chunk = infh.read(MTU)
        sock.sendto(chunk, addr)
        packet_counter += 1
        bytes_counter += len(chunk)
        if len(chunk) < MTU:
            break
        sleep(delay)
    finish = datetime.now()

delta = finish - start
bytes_per_second = bytes_counter / delta.total_seconds()
test_result = {
    'packet_size': MTU,
    'packet_count': npackets,
    'delay': delay,
    'total_bytes': bytes_counter,
    'total_time': delta.total_seconds(),
    'speed': bytes_per_second,
}

if argv[-1] == '-j':
    print(json.dumps(test_result))
else:
    print("sent", packet_counter, "packets")
    print(bytes_counter, "bytes in", delta)
    print(round(bytes_per_second, 2), "bytes/s")

