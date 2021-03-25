#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import random
import threading
import tkinter as tk
from tkgui import Application


class Player(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def action(self):
        result = random.choice(['rock', 'papper', 'scissors'])
        return result


class Game(threading.Thread):
    def __init__(self, player1, player2):
        #threading.Thread.__init__(self)       
        super().__init__()
        self.player1 = player1
        self.player2 = player2

        self.result1 = None
        self.result2 = None
        self.result = None

        self.observer = None
        print('init')


    def notify(self):
        if self.observer:
            self.observer.update(self)

    def go_one_round(self):
        self.result1 = self.player1.action()
        self.result2 = self.player2.action()
        c = (self.result1, self.result2)
        pattern1win = [('rock', 'scissors'), ('scissors', 'papper'), ('papper', 'rock')]
        pattern2win = [('scissors', 'rock'), ('papper', 'scissors'), ('rock', 'papper')]

        if c in pattern1win:
            return self.player1 

        if c in pattern2win:
            return self.player2

        return None


    def run(self):
        print('run')
        #for _ in range(1,10):
        while True:
            self.result = self.go_one_round()
            print(self.result)
            self.notify()

            time.sleep(1)


def main():
    a = Player('Adam')
    b = Player('Handy')
    g = Game(a, b)
    print(g)

    root = tk.Tk()
    gui = Application(root)

    g.observer = gui 
    g.start()

    root.mainloop()


if __name__ == "__main__":
    main()
