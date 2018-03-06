import time
import curses
import RPi.GPIO as GPIO


def main():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.OUT)
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(15, GPIO.OUT)

    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    screen.nodelay(True)
    action_timestamp = time.time()
    try:
        while True:
            char = screen.getch()
            if char == ord('q'): 
                break
            elif char == curses.KEY_UP:
                print('up')
                GPIO.output(7, False)
                GPIO.output(11, True)
                GPIO.output(13, False)
                GPIO.output(15, True)
                action_timestamp = time.time()
            elif char == curses.KEY_DOWN:
                print('down')
                GPIO.output(7, True)
                GPIO.output(11, False)
                GPIO.output(13, True)
                GPIO.output(15, False)
                action_timestamp = time.time()
            elif char == curses.KEY_RIGHT:
                print('right')
                GPIO.output(7, True)
                GPIO.output(11, False)
                GPIO.output(13, False)
                GPIO.output(15, True)
                action_timestamp = time.time()
            elif char == curses.KEY_LEFT:
                print('left')
                GPIO.output(7, False)
                GPIO.output(11, True)
                GPIO.output(13, True)
                GPIO.output(15, False)
                action_timestamp = time.time()
            elif char == 10:
                print('stop')
                GPIO.output(7, False)
                GPIO.output(11, False)
                GPIO.output(13, False)
                GPIO.output(15, False)
            else:
                if time.time() - action_timestamp > 0.5:
                    print('release')
                    GPIO.output(7, False)
                    GPIO.output(11, False)
                    GPIO.output(13, False)
                    GPIO.output(15, False)
                    action_timestamp = time.time()
    finally:
        curses.nocbreak()
        screen.keypad(0)
        curses.echo()
        curses.endwin()

if __name__ == '__main__':
    main()
