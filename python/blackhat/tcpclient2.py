#!/usr/bin/env python3

import socket

def main():
    target = ('0.0.0.0', 9999)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(target)
    client.send(b'abc')
    resp = client.recv(4096)
    print(resp)


if __name__ == '__main__':
    main()

