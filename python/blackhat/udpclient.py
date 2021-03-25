#!/usr/bin/env python3

import socket

def main():
    target = ('127.0.0.1', 80)

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto(b'AABBCC', target)
    resp, addr = client.recvfrom(4096)
    print(resp)


if __name__ == '__main__':
    main()

