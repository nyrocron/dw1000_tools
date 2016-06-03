#!/usr/bin/env python3

# Copyright (c) 2016 Florian Tautz <dev@nyronet.de>

from time import sleep
from sys import argv, stdin, stdout, stderr
from datetime import datetime

delay = 0.013
burst_size = 950
burst_count = 1000

if len(argv) > 1:
    delay = float(argv[1])

start = datetime.now()

for i in range(burst_count):
    data = stdin.read(burst_size)
    stdout.write(data)
    sleep(delay)

end = datetime.now()
delta = end - start
print("piped through {0} bytes in {1}".format(burst_size * burst_count, delta), file=stderr)

