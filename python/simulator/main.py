#!/usr/bin/env python3
import random
import time
import curses
from curses import wrapper
import datetime

#def main(stdscr):
def main():
    stdscr = curses.initscr()

    stdscr.clear()
    #stdscr.nodelay(True)

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

    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

#wrapper(main)
main()
