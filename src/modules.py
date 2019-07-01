from datetime import datetime, timedelta
from urllib.request import urlopen, urlretrieve
from urllib.error import HTTPError
from random import randint
from PIL import ImageTk, Image
import json

from utility import *


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


class StarModule:
    def __init__(self, canvas, x, y, w, h, p):
        self.canvas = canvas
        self.x, self.y, self.w, self.h, self.p = x, y, w, h, p
        self.stars = []
        self.star_refs = []
        for i in range(0, 100):
            sx, sy, sz = randint(0, w), randint(0, h), randint(-p, 0)
            star = Star(sx, sy, sz, 50)
            self.stars.append(star)
            render_loc = self.offset(*get_2d(sx, sy, sz, self.w, self.h, self.p))
            scaled_r = get_scaled_r(star.r, sz, self.p)
            ref = self.canvas.create_oval(*get_circle(*render_loc, scaled_r), fill="#ffffff", width=0)
            self.star_refs.append(ref)
        self.mainloop()

    def offset(self, x, y):
        return self.x + x, self.y + y

    def update(self):
        for star in self.stars:
            star.set(z=star.z + star.v)
            if star.z > 0:
                star.x, star.y = randint(0, self.w), randint(0, self.h)
                star.z = -self.p

    def render(self):
        for i, star in enumerate(self.stars):
            render_loc = self.offset(*get_2d(star.x, star.y, star.z, self.w, self.h, self.p))
            scaled_r = get_scaled_r(star.r, star.z, self.p)
            self.canvas.coords(self.star_refs[i], get_circle(*render_loc, scaled_r))

    def mainloop(self):
        self.update()
        self.render()
        self.canvas.after(20, self.mainloop)


class Star:
    def __init__(self, x, y, z, v):
        self.x, self.y, self.z, self.v = x, y, z, v
        self.r = 4

    def set(self, x=None, y=None, z=None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if z is not None:
            self.z = z

    def get_loc(self):
        return self.x, self.y, self.z
