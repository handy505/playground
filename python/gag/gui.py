import tkinter as tk
import os
import math
import threading
import time

class View(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.parent.wm_title('Tkinter MVC Demo')
        self.parent.wm_geometry('800x600')


        self.area = tk.StringVar()
        self.area.set('Circle information')
        lbl = tk.Label(self.parent, text='hello', textvariable=self.area, fg='red', anchor=tk.W, font='TkFixedFont')
        lbl.pack()

    def update(self, subject, *args, **kwargs):
        msg = 'Circle: ({}, {}), r: {}, Area: {}'.format(subject.x, subject.y, subject.r, subject.area())
        self.area.set(msg)


class Model(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.x = 0
        self.y = 0
        self.r = 1
        print(self.area())


    def area(self):
        return math.pi * self.r * self.r
    
    def add_observer(self, observer):
        self.observer = observer

    def notify(self):
        if self.observer:
            self.observer.update(self)

    def run(self):
        print(self.area())
        while True:
            self.r += 1  
            print('r = {}, area = {}'.format(self.x, self.area()))
            self.notify()
            time.sleep(1)





if __name__ == '__main__':

    view = View(tk.Tk())

    model = Model()
    model.add_observer(view)

    model.start()
    tk.mainloop()
