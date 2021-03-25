#!/usr/bin/env python3

import socket
import threading

def handle_client(client_socket):
    resp = client_socket.recv(1024)
    print('received: {}'.format(resp))
    client_socket.send(b'ack')
    client_socket.close()


def main():
    ip   = '0.0.0.0'
    port = 9999

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    print('listening on {}:{}'.format(ip, port))
    server.listen(5)


    while True:
        client, addr = server.accept()
        print('accept connection from {}'.format(addr))
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()




if __name__ == '__main__':
    main()

