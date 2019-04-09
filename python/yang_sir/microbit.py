# Add your Python code here. E.g.
from microbit import *
import utime
import music

def main():
    threshold = 1000 * 60 * 6
    #threshold = 1000 * 30
    start = utime.ticks_ms()
    while True:
        
        now = utime.ticks_ms()
        
        seconds = now // 1000
        if seconds % 2 == 0: display.show(Image.CLOCK3)
        else:                display.show(Image.CLOCK9)
        
        beep1 = utime.ticks_ms()
        beep2 = beep1 + 200
        while utime.ticks_diff(now, start) > threshold:
            buzz_start = now
            display.show(Image.HEART)
          
            # beep  
            if utime.ticks_diff(utime.ticks_ms(), beep1) > 0:
                music.pitch(1760, 100, wait=False)
                beep1 = beep1 + 2000
                
            # beep    
            if utime.ticks_diff(utime.ticks_ms(), beep2) > 0:
                music.pitch(1760, 100, wait=False)
                beep2 = beep2 + 2000
                
            # button
            if button_a.is_pressed():
                action = utime.ticks_ms()
                spend = utime.ticks_diff(action, buzz_start)
                display.scroll(str(spend))
                if spend < 3000: threshold = 1000 * 60 * 6
                else:            threshold = 1000 * 60 * 3
                #if spend < 3000: threshold = 1000 * 30
                #else:            threshold = 1000 * 10
                start = utime.ticks_ms()
                break

        sleep(1000)


def buzz():
    while True:
        pin0.write_digital(1)
        sleep(1)
        pin0.write_digital(0)
        sleep(1)
        

def beep():
    music.pitch(1760, 100)
    sleep(200)
    music.pitch(1760, 100)
    sleep(200)
    
def sound():
    music.play(music.DADADADUM)
    music.play(music.ENTERTAINER)
    music.play(music.PRELUDE)
    music.play(music.ODE)
    music.play(music.NYAN)
    music.play(music.RINGTONE)
    music.play(music.FUNK)
    music.play(music.BLUES)
    music.play(music.BIRTHDAY)
    music.play(music.WEDDING)
    music.play(music.FUNERAL)
    music.play(music.PUNCHLINE)
    music.play(music.PYTHON)
    music.play(music.BADDY)
    music.play(music.CHASE)
    music.play(music.BA_DING)
    
    music.play(music.WAWAWAWAA)
    music.play(music.JUMP_UP)
    music.play(music.JUMP_DOWN)
    music.play(music.POWER_UP)
    music.play(music.POWER_DOWN)
    

        
if __name__ == '__main__':
    main()
    #sound()    