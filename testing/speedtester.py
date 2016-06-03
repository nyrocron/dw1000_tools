#!/usr/bin/env python3

# Copyright (c) 2016 Florian Tautz <dev@nyronet.de>

import re
import subprocess
from time import sleep
import json
import numpy as np
from sys import stderr

default_config = {
    'CLIENT_HOST': 'pa',
    'SERVER_HOST': 'pb',
    'SERVER_IP': '10.0.0.2',
    'SERVER_PORT': '1785',
    'PROCESS_TIMEOUT': 60,
}

def run_test(packet_size, delay, packet_count=1000, cfg=default_config):
    server_process = subprocess.Popen("ssh {0} './speedtest_server.py {1} {2} -j'".format(
                cfg['SERVER_HOST'],
                cfg['SERVER_IP'],
                cfg['SERVER_PORT']),
            stdout=subprocess.PIPE,
            shell=True)
    sleep(1)
    client_process = subprocess.Popen("ssh {0} './speedtest_client.py {1} {2} {3} {4} {5} -j'".format(
                cfg['CLIENT_HOST'],
                cfg['SERVER_IP'],
                cfg['SERVER_PORT'],
                delay,
                packet_count,
                packet_size),
            stdout=subprocess.PIPE,
            shell=True)

    client_process.wait(cfg['PROCESS_TIMEOUT'])
    server_process.wait(cfg['PROCESS_TIMEOUT'])

    client_result = json.loads(client_process.stdout.read().decode('utf-8'))
    server_result = json.loads(server_process.stdout.read().decode('utf-8'))

    print("client", client_result)
    print("server", server_result)

    return (
            client_result['packet_size'],
            client_result['delay'],
            client_result['speed'],
            server_result['speed'],
            server_result['packet_count'] / client_result['packet_count'],
            client_result['packet_count'],
    )

if __name__ == '__main__':

    presets = {
        'largepacket': {
            'packsize': [710, 970+1, 20],
            'delay': [0.0025, 0.004+0.0001, 0.0001],
            'packet_count': 1000,
        },
        'largepacket_1m': {
            'packsize': [750, 950+1, 50],
            'delay': [0.006, 0.012+0.0001, 0.0002],
            'packet_count': 500,
        },
        'llong': {
            'packsize': [710, 970+1, 20],
            'delay': [0.004, 0.01+0.0001, 0.0005],
            'packet_count': 1000,
        },
        'llong_long': {
            'packsize': [950, 970+1, 20],
            'delay': [0.000, 0.01+0.0001, 0.0005],
            'packet_count': 1000,
        },
        'lquick': {
            'packsize': [710, 970+1, 20],
            'delay': [0.004, 0.01+0.0001, 0.0005],
            'packet_count': 50,
        },

        'lq_inter': {
            'packsize': [950, 950 + 1],
            'delay': [0.002, 0.005, 0.0005],
            'packet_count': 100,
        },

        'widerange': {
            'packsize': [100, 950+1, 50],
            'delay': [0.0005, 0.005+0.0001, 0.0005],
            'packet_count': 1000,
        },
        'quick': {
            'packsize': [100, 900+1, 200],
            'delay': [0.001, 0.005+0.0001, 0.001],
            'packet_count': 100,
        },
    }

    from sys import argv
    from datetime import datetime

    if len(argv) > 1:
        preset = argv[1]
    else:
        preset = 'quick'

    if len(argv) > 2:
        testname = '{0}_{1}'.format(preset, argv[2])
    else:
        testname = preset

    packsize_range = presets[preset]['packsize']
    delay_range = presets[preset]['delay']
    pack_count = presets[preset]['packet_count']

    results = [(
            'packet_size',
            'delay',
            'speed_sender',
            'speed_receiver',
            'link_quality',
            'packets_sent',
    )]

    for psize in np.arange(*packsize_range):
        for pdelay in np.arange(*delay_range):
            result = run_test(psize, pdelay, pack_count)
            print(result, file=stderr)
            results.append(result)

    out_fn = '{0}_{1}.csv'.format(testname, datetime.now().strftime('%Y-%m-%d_%H-%M'))
    with open(out_fn, 'w') as out_fh:
        for row in results:
            print(';'.join([str(x) for x in row]), file=out_fh)

