from tkinter import *
from datetime import datetime


class App:
    def __init__(self, master):
        self.canvas = Canvas(master, width=960, height=540, background="#000000")
        self.canvas.pack()
        self.hh, self.mm, self.ss, self.ms = 0, 0, 0, 0
        self.time_text = self.canvas.create_text((480, 270), fill="#00ff00", font=("Arial", 20), text=self.get_time_text())
        self.mainloop()

    def update(self):
        self.hh = datetime.today().hour
        self.mm = datetime.today().minute
        self.ss = datetime.today().second
        self.ms = round(datetime.today().microsecond / 1000)

    def render(self):
        self.canvas.itemconfig(self.time_text, text=self.get_time_text())

    def mainloop(self):
        self.update()
        self.render()
        self.canvas.after(1, self.mainloop)

    def get_time_text(self):
        hh_text = self.hh if self.hh > 9 else "0{}".format(self.hh)
        mm_text = self.mm if self.mm > 9 else "0{}".format(self.mm)
        ss_text = self.ss if self.ss > 9 else "0{}".format(self.ss)
        ms_text = self.ms if self.ms > 99 else \
            "0{}".format(self.ms) if self.ms > 9 else "00{}".format(self.ms)
        return "{}:{}:{}.{}".format(hh_text, mm_text, ss_text, ms_text)


root = Tk()
app = App(root)
root.mainloop()
