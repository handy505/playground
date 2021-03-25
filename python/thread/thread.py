#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import threading
import queue
import time

class BuzzThread(threading.Thread):
    def __init__(self, que):
        threading.Thread.__init__(self)
        self.que = que
        self.duty= (0, 1)

    def run(self):
        while True:
            if not self.que.empty():
                self.duty = self.que.get()
            print('buzz on {} sec at {}'.format(self.duty[0], time.time()))
            time.sleep(self.duty[0])
            print('buzz off {} sec at {}'.format(self.duty[1], time.time()))
            time.sleep(self.duty[1])
            


def main():
    q = queue.Queue()
    q.put((1,2))
    b = BuzzThread(q)
    b.start()
    print('main function is in buzy... at {}'.format(time.time()))
    time.sleep(10)
    q.put((3,4))
    time.sleep(10)
    print('main function is finish... at {}'.format(time.time()))



if __name__ == '__main__':
    main()
