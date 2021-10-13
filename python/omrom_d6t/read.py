import sys
import time
import threading

import numpy as np
import zmq


class D6TReceiver(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)       
        self.heatmap = np.zeros([32, 32], np.float)
        self.heatmap2 = np.copy(self.heatmap)

        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind('tcp://*:5555')


    def run(self):
        row = 0
        for line in sys.stdin:

            if 'Temperature' in line:
                row = 0
                continue 
            else:
                row += 1
                
            line = line.rstrip('\n')
            line = line.rstrip(' [degC]') 
            line = line.rstrip(' ')
            line = line.rstrip(',')
            #print('Python({}): {}'.format(row, line))
        
            values = line.split(',')
            for i, v in enumerate(values):
                col = i
                self.heatmap[row-1, col] = float(v)

            if row == 32:
                self.heatmap2 = np.copy(self.heatmap)
                self.send()

    def send(self):
        with np.printoptions(threshold=sys.maxsize, suppress=True):
            lst2d = self.heatmap2.tolist()

            lines = []
            for lst in lst2d:
                elements = [str(e) for e in lst]
                line = ','.join(elements)
                lines.append(line)

            s = '\n'.join(lines)

            print(s)
            self.socket.send_string(s)



class Viewer(object):
    def __init__(self, source):
        self.source = source

    def update(self):
        with np.printoptions(threshold=sys.maxsize, suppress=True):
            lst2d = self.source.heatmap2.tolist()
            for lst in lst2d:
                print(lst)
            print('\n\n')


if __name__ == '__main__':

    r = D6TReceiver()
    r.start()

    '''while True:
        v = Viewer(r)
        v.update()
        time.sleep(0.5)
        '''

    r.join()
