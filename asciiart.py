# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 23:58:05 2018
Apologies for the bad code, and dear god is some of it bad...
@author: Ryan
"""

from PIL import Image as PILImg
from tkinter import *
from PIL import Image, ImageFont, ImageDraw
from operator import itemgetter
import sys
import os.path
import threading

test = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!\"£$%^&*()-_=+`¬#~'@;:/?.>,<\\| ")
cor = ImageFont.truetype(r"cour.ttf", 12)

def generateImg(char, font):
    im = Image.new("RGBA", font.getsize(char), (0, 0, 0))
    draw = ImageDraw.Draw(im)
    draw.text((0, 0), char, (255, 255, 255), font=font)
    return im

def getDensity(image):
    t = 0
    for x in range(image.width):
        for y in range(image.height):
            p = image.getpixel((x, y))
            t += round((p[0] + p[1] + p[2]) /3)
    return t / (image.width * image.height)

output = []
for char in test:
    output += [(char, getDensity(generateImg(char, cor)))]
output = sorted(output, key=itemgetter(1))

def toASCII(in_file, out_file="ascii.txt", rotation=0):
    im = PILImg.open(in_file).convert("RGB")
    im = im.rotate(rotation)
    with open(out_file, "w") as f:
        for h in range(0, im.height, 2):
            for w in range(im.width):
                f.write(getChar(toHSL(im.getpixel((w, h)))[2]))
            f.write("\n")
    
def toHSL(rgb):
    rgb_f = list(map(lambda x: x / 255, rgb))
    margb, mirgb = max(rgb_f), min(rgb_f)
    if margb - mirgb == 0:
        h = 0
    else:
        if rgb_f[0] == margb:
            h = (rgb_f[1] - rgb_f[2]) / (margb - mirgb)
        if rgb_f[1] == margb:
            h = 2.0 + ((rgb_f[2] - rgb_f[0])/(margb - mirgb))
        if rgb_f[2] == margb:
            h = 4.0 + ((rgb_f[0] - rgb_f[1]) / (margb - mirgb))
    h = round(h * 60)
    if h < 0:
        while h < 0:
            h += 360
    l = round(((mirgb + margb) / 2) * 100)
    if margb - mirgb == 0:
        s = 0
    else:
        if l < 50:
            s = (margb - mirgb) / (margb + mirgb)
        else:
            s = (margb-mirgb) / (2.0 - margb - mirgb)
    s = round(s * 100)
    return (h, s, l)

def getChar(l):
    index = round(l/(100/len(output)))
    if index >= len(output):
        index = len(output) - 1
    return output[index][0]

class App:

    def __init__(self, master):
        Label(master, text="Input file").grid(row=0, column=0)
        Label(master, text="Output file").grid(row=1, column=0)
        Label(master, text="Rotation factor").grid(row=2, column=0)
        
        vcmd = (master.register(self.validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        
        self.invar = StringVar()
        self.outvar = StringVar()
        self.rotvar = StringVar()
        
        self.outvar.set("ascii.txt")
        self.rotvar.set("0")
        
        self.infile = Entry(master, textvariable=self.invar)
        self.outfile = Entry(master, textvariable=self.outvar)
        self.rotationentry = Entry(master, validate = 'key', validatecommand = vcmd, textvariable=self.rotvar)
        
        self.error = Label(master, text="")
        self.error.grid(row=3, column=0, columnspan=2)
        
        self.infile.grid(row=0, column=1, sticky=N+S+E+W)
        self.outfile.grid(row=1, column=1, sticky=N+S+E+W)
        self.rotationentry.grid(row=2, column=1, sticky=N+S+E+W)
        
        self.run = Button(master, text="Run", command=self.execute_ascii)
        self.run.grid(row=4, column=0, sticky=N+S+E+W, columnspan=2)
        
    def execute_ascii(self):
        if self.outfile.get() == "":
            self.outfile.config(text="ascii.txt")
        if self.infile.get() != "":
            if os.path.isfile(self.infile.get()):
                r = 0
                if self.rotationentry.get() == "":
                    self.error.config(text="Rotation assumed to be 0")
                else:
                    r = float(self.rotationentry.get())
                toASCII(self.infile.get(), self.outfile.get(), r)
                self.error.config(text="Complete")
            else:
                self.error.config(text="Input file does not exist")
        else:
            self.error.config(text="Input file must be specified")
        pass
    
    def validate(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed == "":
            return True
        if text in '0123456789.-+':
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False
        
root = Tk()
root.grid_columnconfigure(1, weight=1)
root.title("ASCII Art")
app = App(root)
root.mainloop()