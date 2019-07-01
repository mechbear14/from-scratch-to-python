from datetime import datetime, timedelta
from urllib.request import urlopen, urlretrieve
from urllib.error import HTTPError
from random import randint
from PIL import ImageTk, Image
import json


class ClockModule:
    def __init__(self, canvas, x, y, w, h):
        self.canvas = canvas
        self.x, self.y, self.w, self.h = x, y, w, h
        self.hh, self.mm, self.ss, self.ms = 0, 0, 0, 0
        self.time_text = self.canvas.create_text((self.x + self.w / 2, self.y+ self.h / 2),
                                                 fill="#00ff00", font=("Arial", 20),
                                                 text=self.get_time_text())

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


class GalleryModule:
    def __init__(self, canvas, x, y, w, h):
        self.canvas = canvas
        self.x, self.y, self.w, self.h = x, y, w, h
        self.image_box = None
        self.image_ref = None
        self.image = None
        self.mainloop()

    def update(self):
        delta_date = randint(0, 90)
        date = datetime.today() - timedelta(days=delta_date)
        date_string = "{}-{}-{}".format(date.year,
                                        date.month if date.month > 9 else "0{}".format(date.month),
                                        date.day if date.day > 9 else "0{}".format(date.day))
        url = "https://api.nasa.gov/planetary/apod?date={}&api_key={}".format(date_string, "DEMO_KEY")
        try:
            with urlopen(url) as response:
                string = response.read().decode("utf-8")
                image_url = json.loads(string)["url"]

                urlretrieve(image_url, "temp.jpg")
        except HTTPError:
            print("Roar! No gallery for you!")

        try:
            self.image = Image.open("temp.jpg")
        except OSError:
            pass

    def render(self):
        if self.image_box is not None:
            self.canvas.delete(self.image_box)
        self.image = self.image.resize((self.w, self.h))
        self.image_ref = ImageTk.PhotoImage(self.image)
        self.image_box = self.canvas.create_image((self.x + self.w / 2, self.y + self.h / 2), image=self.image_ref)

    def mainloop(self):
        self.update()
        self.render()
        self.canvas.after(60000, self.mainloop)
