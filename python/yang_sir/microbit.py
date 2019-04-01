# Add your Python code here. E.g.
from microbit import *
import utime

def main():
    
    start = utime.ticks_ms()
    display.show(Image.SAD)
    threshold = 1000 * 60 * 6
    while True:
        
        now = utime.ticks_ms()
        
        seconds = now // 1000
        if seconds % 2 == 0:
            display.show(Image.CLOCK3)
        else:
            display.show(Image.CLOCK9)
        
        while utime.ticks_diff(now, start) > threshold:
            buzz = now
            display.show(Image.HEART)
            if button_a.is_pressed():
                action = utime.ticks_ms()
                spend = utime.ticks_diff(action, buzz)
                display.scroll(str(spend))
                if spend < 3000: threshold = 1000 * 60 * 6
                else:            threshold = 1000 * 60 * 3
                start = utime.ticks_ms()
                break
         
            
            
        sleep(1000)


def buzz():
    while True:
        pin0.write_digital(1)
        sleep(1)
        pin0.write_digital(0)
        sleep(1)
        
if __name__ == '__main__':
    #main()
    buzz()
    