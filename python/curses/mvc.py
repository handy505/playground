#!/usr/bin/env python3
import random
import time
import curses
from curses import wrapper
import datetime

import signal
import sys
import atexit

# ---------------------------------------------------
class View(object):
    def __init__(self, stdscr):
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

                
# ---------------------------------------------------
class Model(object):
    def __init__(self):
        self.value = 1
        self.observer = None 

    def add_observer(self, obs):
        self.observer = obs

    def notify(self):
        self.observer.update(self)

    def increment(self):
        self.value += 1
        self.notify()

    def reset_value(self):
        self.value = 0
        self.notify()

# ---------------------------------------------------
class Controller(object):
    def __init__(self, view, model, stdscr):
        self.view = view
        self.model = model
        self.stdscr = stdscr
        self.stdscr.nodelay(True)    

    def run(self):
        while True:
            m.increment()

            c = self.stdscr.getch()
            if c != -1:
                print(c)
                if c == ord('q'):
                    break
                elif c == ord('r'):
                    m.reset_value()

            time.sleep(0.1)


# ---------------------------------------------------
def signal_handler(sig, frame):
    print('signal_handler')
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

    sys.exit(0)

def restore_screen():
    print(sys._getframe().f_code.co_name)
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()



if __name__ == '__main__':
    '''
    Keywords:
        signal
        atexit
        curses nonblocking input

    '''

    #signal.signal(signal.SIGINT, signal_handler)
    atexit.register(restore_screen)

    stdscr = curses.initscr()

    v = View(stdscr)

    m = Model()
    m.add_observer(v)

    c = Controller(model=m, view=v, stdscr=stdscr)
    c.run()
    


    '''curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    '''





