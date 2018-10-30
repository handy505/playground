import tkinter as tk


root = tk.Tk()
text = tk.Text(root)
text.insert(tk.INSERT, 'Hello')
text.insert(tk.INSERT, 'abc')
text.insert(tk.END, 'end')
text.pack()


text.tag_add("here", "1.0", "1.4")
text.tag_add("start", "1.8", "1.13")
text.tag_config("here", background="yellow", foreground="blue")
text.tag_config("start", background="black", foreground="green")
s = text.get(1.0,tk.END)
print(s)
root.mainloop()
