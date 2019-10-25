import tkinter as tk
import os
import math

class View(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.parent.wm_title('Tkinter MVC Demo')
        self.parent.wm_geometry('800x600')

        self.controller = controller

        self.area = tk.StringVar()
        self.area.set('Circle information')
        lbl = tk.Label(self.parent, text='hello', textvariable=self.area, fg='red', anchor=tk.W, font='TkFixedFont')
        lbl.pack()
        btn1 = tk.Button(self.parent, text='Inc', command=self.controller.handle_inc_press)
        btn1.pack()
        btn2 = tk.Button(self.parent, text='Dec', command=self.controller.handle_dec_press)
        btn2.pack()

    def update(self, subject, *args, **kwargs):
        msg = 'Circle: ({}, {}), r: {}, Area: {}'.format(subject.x, subject.y, subject.r, subject.area())
        self.area.set(msg)


class Model(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.r = 1

    def area(self):
        return math.pi * self.r * self.r
    
    def add_observer(self, observer):
        self.observer = observer

    def notify(self):
        if self.observer:
            self.observer.update(self)


class Controller(object):  
    def __init__(self):
        parent = tk.Tk()
        self.view = View(parent, self)

        self.model = Model()
        self.model.add_observer(self.view)

        tk.mainloop()

    def handle_inc_press(self):
        print('inc')
        self.model.r += 1
        self.model.notify()

    def handle_dec_press(self):
        print('dec')
        self.model.r -= 1
        self.model.notify()


if __name__ == '__main__':
    c = Controller()

