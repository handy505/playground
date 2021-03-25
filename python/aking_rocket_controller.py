#!/usr/bin/env python3

import time
import json
import socket
from simple_pid import PID

pid = PID(1, 1, 0.5, setpoint=30)
pid.output_limits = (0, 30)
#pid.sample_time = 0.01

def main():
    target = ('127.0.0.1', 9999)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(target)


    #v = controlled_system.update(0)


    pid.tunings = (12, 30, 20)

    while True:
        resp = client.recv(62)
        s = resp.decode('utf-8')

        try:
            dt = json.loads(s)
            target = dt.get('TargetY')
            height = dt.get('RocketY')
        except json.decoder.JSONDecodeError as err:
            continue

        pid.setpoint = target
        output = pid(float(height))
        print('{}, {}'.format(height, output))

        dtout = {"JetPower": output}
        s = json.dumps(dtout)
        client.send(s.encode('utf-8'))








if __name__ == '__main__':
    main()

