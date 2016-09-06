#!/usr/bin/env python3
import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        #self.pack()
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        '''
        self.btn1 = tk.Button(self)
        self.btn1["text"] = "hello world]\n(click me)"
        self.btn1["command"] = self.say_hi
        self.btn1.pack(side="top")

        self.btn2 = tk.Button(self, text="i'm handy", fg="orange", bg="White")
        self.btn2.pack(side="top")

        self.lbl1 = tk.Label(self, text="it's a label")
        self.lbl1.pack(side="top")

        self.QUIT = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
        self.QUIT.pack(side="bottom")
        '''

        self.label1 = tk.Label(self, text="i'm label1").grid(row=0)
        self.label2 = tk.Label(self, text="i'm label2").grid(row=1)
        self.e1 = tk.Entry(self).grid(row=0, column=1)
        self.e3 = tk.Entry(self).grid(row=0, column=2)
        self.e2 = tk.Entry(self).grid(row=1, column=1,
                                      columnspan=2, sticky=tk.EW)
        self.label3 = tk.Label(self, text="i'm label3", relief=tk.SUNKEN)
        self.label3.grid(row=2, columnspan=2, sticky=tk.EW)
        #
        # self.t1 = tk.Text(self).grid(row=2, column=1)



    def say_hi(self):
        print("hello everyone")


root = tk.Tk()
app = Application(master=root)
app.mainloop()
