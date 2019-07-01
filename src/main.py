from tkinter import *


class App:
    def __init__(self, master):
        self.canvas = Canvas(master, width=960, height=540, background="#000000")
        self.canvas.pack()


root = Tk()
app = App(root)
root.mainloop()
