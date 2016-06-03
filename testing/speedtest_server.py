#!/usr/bin/env python3

# Copyright (c) 2016 Florian Tautz <dev@nyronet.de>

import socket
from sys import argv
from datetime import datetime, timedelta
import json

MTU = 1000
TIMEOUT = 1.0
INIT_TIMEOUT = timedelta(seconds=30)

addr = (argv[1], int(argv[2]))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(addr)

sock.settimeout(TIMEOUT)

packets = []

start = datetime.now()
while True:
    try:
        data, addr = sock.recvfrom(MTU)
        ts = datetime.now()
        packets.append((ts, addr, data))
    except socket.timeout:
        if len(packets) > 0 or datetime.now() - start > INIT_TIMEOUT:
            break


total_bytes = sum([len(data) for _, _, data in packets])
if len(packets) > 0:
    delta = packets[-1][0] - packets[0][0]
    bytes_per_second = (total_bytes - len(packets[0][2])) / delta.total_seconds()
else:
    delta = 0
    bytes_per_second = 0

test_result = {
    'packet_count': len(packets),
    'total_bytes': total_bytes,
    'total_time': delta.total_seconds(),
    'speed': bytes_per_second,
}

if argv[-1] == '-j':
    print(json.dumps(test_result))
else:
    print("received", len(packets), "packets")
    print(total_bytes, "bytes in", delta)
    print(round(bytes_per_second, 2), "bytes/s")

