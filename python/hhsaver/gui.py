#!/usr/bin/env python3
from tkinter import *
import tkFont

helv36 = tkFont.Font(family="Helvetica",size=36,weight="bold")

def onclick():
   pass


def gui():
    root = Tk()
    text = Text(root)
    text.insert(INSERT, "Hello.....")
    text.insert(END, "Bye Bye.....")
    text.font(helv36)
    text.pack()

    text.tag_add("here", "1.0", "1.4")
    text.tag_add("start", "1.8", "1.13")
    text.tag_config("here", background="yellow", foreground="blue")
    text.tag_config("start", background="black", foreground="green")
    root.mainloop()

if __name__ == "__main__":
    gui()

'''
class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        #self.grid()
        self.createWidgets()

    def createWidgets(self):
        #self.quitButton = tk.Button(self, text='Quit',command=self.quit)
        #self.quitButton.grid()

        c = tk.Canvas(self, bg="blue", height=250, width=300)

        coord = 10, 50, 240, 210
        arc = c.create_arc(coord, start=0, extent=150, fill="red")

        c.pack()

app = Application()
app.master.title('Sample application')
app.mainloop()'''

'''
root = Tk()
root.title("abc")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

ttk.Label(mainframe, text="get off work").grid(column=3, row=1, sticky=W)

root.mainloop()
'''