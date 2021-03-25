#!/usr/bin/env python3

import socket

def main():
    target = ('www.google.com', 80)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(target)
    client.send(b'GET / HTTP/1.1\r\nHost: google.com\r\n\r\n')
    resp = client.recv(4096)
    print(resp)


if __name__ == '__main__':
    main()

