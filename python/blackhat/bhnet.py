#!/usr/bin/env python3
import optparse
import socket
import subprocess
import sys
import threading

def run_command(command):
    command = command.rstrip()

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        output = output.decode('utf-8')
    except Exception as err:
        output = 'run_command exception'
    
    return output


def handle_client_request(client_socket, opts, args):
    if opts.upload_destination:
        file_buffer = '' 
        while True:
            data = client_socket.recv(1024)
            if not data: 
                break
            else:        
                file_buffer += data

        try:
            with open(opts.upload_destination, 'w', encoding='utf-8') as fd:
                fd.write(file_buffer)

            client_socket.send(b'success saved file to {}'.format(opts.upload_destination))

        except Exception as err:
            client_socket.send('fail saved file to {}'.format(opts.upload_destination))

        
    if opts.commandshell:

        while True:
            client_socket.send(b'<BHP:#>')
            
            cmd_buffer = ''
            while '\n' not in cmd_buffer:
                #cmd_buffer += client_socket.recv(1024)
                data = client_socket.recv(1024)
                cmd_buffer += data.decode('utf-8')

            print('cmd_buffer: {}'.format(cmd_buffer))

            shellresp = run_command(cmd_buffer)
            print(shellresp)
            client_socket.send(shellresp.encode('utf-8'))




def server_loop(opts, args):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((opts.target, opts.port))
    print('listening on {}:{}'.format(opts.target, opts.port))
    server.listen(5)

    while True:
        client, addr = server.accept()
        print('accept connection from {}'.format(addr))
        client_thread = threading.Thread(target=handle_client_request, 
                                         args=(client, opts, args, ))
        client_thread.start()



# --------------------------------------------------------------------------------
def client_sender(buffer, opts, args):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientsocket:
        try:
            #clientsocket.connect((opts.target, opts.port))
            clientsocket.connect(('0.0.0.0', opts.port))

            if len(buffer):
                clientsocket.send(buffer.encode('utf-8'))

            while True:

                data = clientsocket.recv(4096)
                print(data.decode('utf-8'), end='')

                buf = input()
                buf = buf + '\n'
                clientsocket.send(buf.encode('utf-8'))
        except Exception as err:
            print(err)


# --------------------------------------------------------------------------------
def main(opts, args):

    if opts.listen:
        server_loop(opts, args)
    else:
        buffer = sys.stdin.read()
        client_sender(buffer, opts, args)


# --------------------------------------------------------------------------------
if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-l', '--listen',
                      action='store_true',
                      dest='listen',
                      help='listen')
    parser.add_option('-e', '--execute',
                      dest='execute',
                      help='execute')
    parser.add_option('-c', '--commandshell',
                      action='store_true',
                      dest='commandshell',
                      help='commandshell')
    parser.add_option('-u', '--upload',
                      dest='upload_destination',
                      help='upload_destination')
    parser.add_option('-t', '--target',
                      dest='target',
                      type='string',
                      default='127.0.0.1',
                      help='target')
    parser.add_option('-p', '--port',
                      dest='port',
                      type='int',
                      default='9999',
                      help='port')
    opts, args = parser.parse_args()
    print(opts)
    print(args)


    main(opts, args)
