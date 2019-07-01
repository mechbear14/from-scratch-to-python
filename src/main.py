from tkinter import *
from modules import ClockModule, GalleryModule


class App:
    def __init__(self, master):
        self.canvas = Canvas(master, width=960, height=540, background="#000000")
        self.canvas.pack()
        self.clock = ClockModule(self.canvas, 80, 150, 320, 240)
        self.clock.mainloop()
        self.gallery = GalleryModule(self.canvas, 480, 135, 480, 270)
        self.gallery.mainloop()


root = Tk()
app = App(root)
root.mainloop()
