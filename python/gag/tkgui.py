import tkinter as tk
from tkinter.font import Font
import tkinter.scrolledtext as tkst
import time
import threading
import datetime
import os
import queue
import subprocess


class MainPage(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player1 = tk.StringVar()
        self.player2 = tk.StringVar()
        self.game    = tk.StringVar()

        self.player1.set('player1')
        self.player2.set('player2')
        self.game.set('game')

        fontstyle = 'TkFixedFont'
        
        lbl = tk.Label(self, anchor=tk.W, font=fontstyle, textvariable=self.player1)
        lbl.pack(side="top", fill="both", expand=False)

        lbl = tk.Label(self, anchor=tk.W, font=fontstyle, textvariable=self.player2)
        lbl.pack(side="top", fill="both", expand=False)

        lbl = tk.Label(self, anchor=tk.W, font=fontstyle, textvariable=self.game)
        lbl.pack(side="top", fill="both", expand=False)


class Application(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lock = threading.RLock()

        self.master.wm_title("Tk GUI")
        self.master.wm_geometry("800x480")
        self.pack(side="top", fill="both", expand=True)

        self.mpage  = MainPage(self)
        buttonframe = tk.Frame(self)
        container   = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        self.mpage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        #self.mpage.show()
        self.mpage.lift()

    def update(self, subject, *args, **kwargs):
        with self.lock:
            s1 = '{}: {}'.format(subject.player1, subject.result1)
            s2 = '{}: {}'.format(subject.player2, subject.result2)
            s3 = 'The Winner is {}'.format(subject.result)
            self.mpage.player1.set(s1)
            self.mpage.player2.set(s2)
            self.mpage.game.set(s3)


if __name__ == "__main__":
    root = tk.Tk()
    Application(root)
    root.mainloop()
