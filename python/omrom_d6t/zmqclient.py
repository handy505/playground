# -*- coding=utf-8 -*-
import zmq
import sys
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://192.168.43.73:5555")
socket.setsockopt_string(zmq.SUBSCRIBE,'')  # 訊息過濾
while True:
    response = socket.recv();
    #print("response: {}".format(response))

    s = response.decode('utf-8')
    lines = s.splitlines()
    for line in lines:
        print(line)

    print('---')


