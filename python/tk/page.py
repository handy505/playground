import tkinter as tk

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def show(self):
        self.lift()

class MainPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.rs485tx = tk.StringVar()
        self.rs485tx.set('RS485 Tx: xx xx xx xx')
        self.rs485rx = tk.StringVar()
        self.rs485rx.set('RS485 Rx: xx xx xx xx')
        self.status = tk.StringVar()
        self.status.set('Status: 99,a,b,c,d,e')

        #f = tkFont.Font(family='Helvetica',size=36,weight='bold')
        tk.Label(self, textvariable=self.rs485tx, anchor=tk.W, font=('Helvetica','16')).pack(side="top", fill="both", expand=False)
        tk.Label(self, textvariable=self.rs485rx, anchor=tk.W).pack(side="top", fill="both", expand=False)
        tk.Label(self, textvariable=self.status, anchor=tk.W).pack(side="top", fill="both", expand=False)

class InverterPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        label = tk.Label(self, text="This is page 2")
        label.pack(side="top", fill="both", expand=True)

class FactoryPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        label = tk.Label(self, text="This is page 3")
        label.pack(side="top", fill="both", expand=True)

class DDCPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        label = tk.Label(self, text="ddc page")
        label.pack(side="top", fill="both", expand=True)

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        mpage = MainPage(self)
        ipage = InverterPage(self)
        fpage = FactoryPage(self)
        dpage = DDCPage(self)

        buttonframe = tk.Frame(self, bg='black')
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        mpage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        ipage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        fpage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        dpage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text='Main Page', command=mpage.lift)
        b2 = tk.Button(buttonframe, text='Inverter Page', command=ipage.lift)
        b3 = tk.Button(buttonframe, text='Factory Page', command=fpage.lift)
        b4 = tk.Button(buttonframe, text='DDC Page', command=dpage.lift)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")
        b4.pack(side="left")

        mpage.show()

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("800x480")
    root.mainloop()
