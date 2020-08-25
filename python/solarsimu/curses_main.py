#!/usr/bin/env python3
import random
import time
import curses
from curses import wrapper
import datetime
import threading


class View(threading.Thread):
    def __init__(self, controller):
        threading.Thread.__init__(self)
        self.controller = controller
        self.stdscr = self.controller.stdscr
        self.stdscr.nodelay(True)
        self.running = True


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
        

    def run(self):        
        while self.running:
            c = self.stdscr.getch()
            if c != -1:
                if c == (ord('q')):
                    self.controller.quit()
                elif c == (ord('i')):
                    self.controller.increment()
                elif c == (ord('d')):
                    self.controller.decrement()




class Model(object):
    def __init__(self, observer):
        self.value = 1
        self.observer = observer

    def notify(self):
        self.observer.update(self)

    def increment(self):
        self.value += 1
        self.notify()

    def decrement(self):
        self.value -= 1
        self.notify()


class Controller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.stdscr = curses.initscr()

        self.view = View(self)
        self.model = Model(self.view)

        self.running = True
    
    def increment(self):
        self.model.increment()

    def decrement(self):
        self.model.decrement()

    def quit(self):
        self.view.running = False
        self.running = False

        self.stdscr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()


    def run(self):
        self.view.start()

        while self.running:
            try:
                #self.model.increment()
                time.sleep(0.1)
            except Exception as err:
                break



if __name__ == '__main__':
    try:
        c = Controller()
        c.start()
        c.join()
    except Exception as err:
        print(err)

