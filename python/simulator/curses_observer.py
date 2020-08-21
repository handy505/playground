#!/usr/bin/env python3
import random
import time
import curses
from curses import wrapper
import datetime

'''def update(stdscr):
    stdscr.clear()
    stdscr.nodelay(True)

    while True:
            
        stdscr.clear()
        stdscr.addstr( 3, 5, str(datetime.datetime.now().replace(microsecond=0)))
        stdscr.addstr(10, 5, str(random.randint(1,100)))
        stdscr.addstr(11, 5, str(random.randint(1,100)))
        stdscr.addstr(12, 5, str(random.randint(1,100)))
        stdscr.addstr(13, 5, str(random.randint(1,100)))
        stdscr.addstr(14, 5, str(random.randint(1,100)))
        stdscr.addstr(15, 5, str(random.randint(1,100)))
        stdscr.addstr(16, 5, '*' * random.randint(1,50))
        stdscr.addstr(20, 5, "Press 'q' to quit")
        stdscr.refresh()

        c = stdscr.getch()
        if c != -1:
            print(c)
            if c == ord('q'):
                break
            
        time.sleep(0.2)
        '''


class View(object):
    def __init__(self, stdscr):
        #self.stdscr = curses.initscr()
        self.stdscr = stdscr

    def update(self, subject):
        self.stdscr.clear()
        self.stdscr.addstr( 3, 5, str(datetime.datetime.now().replace(microsecond=0)))
        self.stdscr.addstr(10, 5, str(random.randint(1,100)))
        self.stdscr.addstr(11, 5, str(random.randint(1,100)))
        self.stdscr.addstr(12, 5, str(random.randint(1,100)))
        self.stdscr.addstr(13, 5, str(random.randint(1,100)))
        self.stdscr.addstr(14, 5, str(random.randint(1,100)))
        self.stdscr.addstr(15, 5, str(random.randint(1,100)))
        self.stdscr.addstr(16, 5, '*' * random.randint(1,50))
        self.stdscr.addstr(17, 5, '*' * subject.value)
        self.stdscr.addstr(20, 5, "Press 'q' to quit")
        self.stdscr.refresh()


    def finish(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()


class Model(object):
    def __init__(self, observer):
        self.value = 1
        self.observer = observer

    def notify(self):
        self.observer.update(self)

    def increment(self):
        self.value += 1
        self.notify()


class Controller(object):
    def __init__(self, view, model):
        self.view = view
        self.model = model
    
if __name__ == '__main__':
    stdscr = curses.initscr()

    v = View(stdscr)
    m = Model(v)

    
    for _ in range(1, 50):
        m.increment()
        time.sleep(0.1)


    v.finish()




    print('-------------------')




