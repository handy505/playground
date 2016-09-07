#!/usr/bin/env python3
from tkinter import *
from tkinter.ttk import *
from tkinter import PhotoImage

def mainview():

    root = Tk()
    myButton = Button(root)
    myImage = PhotoImage(file='cat.gif')
    #myButton.image = myImage
    myButton.configure(image=myImage)
    myButton.pack()
    root.mainloop()

    
if __name__ == "__main__":
    mainview()

