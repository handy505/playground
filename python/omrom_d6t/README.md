
# reference from: 
$ git clone https://github.com/omron-devhub/d6t-2jcieev01-raspberrypi

# modify :
1. modify output format with 32 elements in line

2. use pipeline to cowork with python
$ ./d6t-32l | python3 read.py 

3. python output with zmq over network

4. modify Makefile only for d6t-32l
