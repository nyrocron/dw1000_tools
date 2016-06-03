#!/usr/bin/env python3

# Copyright (c) 2016 Florian Tautz <dev@nyronet.de>

import re
import subprocess

def get_packetloss(ping_lines):
    for line in ping_lines:
        result = re.match(r'.*?(?P<packetloss>\d+)% packet loss', line)
        if result is not None:
            return float(result.group('packetloss')) / 100

def run_ping(host, size=100, count=10, interval=1):
    return subprocess.check_output([
            "ping",
            "-s {0}".format(size),
            "-c {0}".format(count),
            "-i {0}".format(interval),
            host,
            ]).decode('utf-8').split('\n')

if __name__ == '__main__':
    from sys import argv
    from datetime import datetime
    import json

    now = datetime.now()

    cfg = dict()
    
    #target_hostname = argv[1]
    cfg['target_hostname'] = argv[1]

    if len(argv) > 2:
        cfg['interval'] = float(argv[2])
    else:
        cfg['interval'] = 0.2

    if len(argv) > 3:
        cfg['count'] = int(argv[3])
    else:
        cfg['count'] = 100

    if len(argv) > 4:
        cfg['note'] = argv[4]
    else:
        cfg['note'] = target_hostname

    with open("pings.log", "a") as logfile:
        print("[{0}]".format(now.strftime("%Y-%m-%d %H:%M:%S")), json.dumps(cfg), file=logfile)

    out_filename = "ping_{0}_{1}.csv".format(
            cfg['note'],
            now.strftime("%Y-%m-%d_%H-%M-%S"),
    )

    with open(out_filename, "w") as outfh:
        print(";".join(["packet_size", "link_quality"]), file=outfh)
        for i in range(50, 950+1, 50):
            lines = run_ping(
                    cfg['target_hostname'],
                    size=i,
                    count=cfg['count'],
                    interval=cfg['interval'],
            )
            print(";".join([str(i), str(1.0 - get_packetloss(lines))]), file=outfh)

