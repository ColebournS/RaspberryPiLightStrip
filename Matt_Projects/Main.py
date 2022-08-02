# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# Simple test for NeoPixels on Raspberry Pi
import time
import neopixel
import board
import random
import datetime
import tkinter as tk
import sys
# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18
# The number of NeoPixels
num_pixels = 300
# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)
def purpleTealCycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = purpleWheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)
def strobe(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixels[i] = (255,255,255)
        pixels.show()
        time.sleep(wait)
        for i in range(num_pixels):
            pixels[i] = (0,0,0)
        pixels.show()
def purpleWheel(pos):
    if pos < 85:
        b = 255
        r = 0
        g = int(255 - ((255/85)*pos))
    elif pos < 170:
        pos -= 85
        b = 255
        r = int(0 + ((255/85)*pos))
        g = 0
    elif pos <= 255:
        pos -= 170
        b = 255
        r = int(255 - ((255/85)*pos))
        g = int(0 + ((255/85)*pos))
    else:
        r = g = b = 0
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)
def fallColors():
    r = 255
    b = 0
    if ORDER in (neopixel.RGB, neopixel.GRB):
        pixels[random.randint(0, (num_pixels-1))] = (r, random.randint(0, 255), b)
        pixels[random.randint(0, (num_pixels-1))] = (r, random.randint(0, 255), b)
        pixels[random.randint(0, (num_pixels-1))] = (r, random.randint(0, 255), b)
        pixels[random.randint(0, (num_pixels-1))] = (r, random.randint(0, 255), b)
        pixels[random.randint(0, (num_pixels-1))] = (r, random.randint(0, 255), b)
        pixels[random.randint(0, (num_pixels-1))] = (0, 0, 0)
        pixels[random.randint(0, (num_pixels-1))] = (0, 0, 0)
        pixels[random.randint(0, (num_pixels-1))] = (0, 0, 0)
        pixels.show()
    else:
        pixels[random.randint(0, (num_pixels-1))] = (r, random.randint(0, 255), b, 0)
        pixels[random.randint(0, (num_pixels-1))] = (r, random.randint(0, 255), b, 0)
        pixels[random.randint(0, (num_pixels-1))] = (r, random.randint(0, 255), b, 0)
        pixels[random.randint(0, (num_pixels-1))] = (r, random.randint(0, 255), b, 0)
        pixels[random.randint(0, (num_pixels-1))] = (r, random.randint(0, 255), b, 0)
        pixels[random.randint(0, (num_pixels-1))] = (0, 0, 0, 0)
        pixels[random.randint(0, (num_pixels-1))] = (0, 0, 0, 0)
        pixels[random.randint(0, (num_pixels-1))] = (0, 0, 0, 0)
        pixels.show()

def trail():
    r = g = b = 255
    if r == g == b == 255:
        r -=1
    elif r == g == b == 0:
        r += 1
        g += 1
        b += 1
    elif r == 0:
        g -= 1
    elif g == 0:
        b -= 1

def ColorTrail():
    i = 0
    r = 255
    g = b = 0
    while i <= (num_pixels - 1):
        if datetime.time(22) < datetime.datetime.now().time():
            break
        fade = 5/50
        blankPixel = i - 1 if i != 0 else 299
        pixels[blankPixel-1] = (0, 0, 0)
        if r == g or r == b or b == g:
            purpleFade = True if r == 255 and b == g == 0 else False
            blueFade = True if r == b == 255 and g == 0 else False
            tealFade = True if b == 255 and g == r == 0 else False
            greenFade = True if b == g == 255 and r == 0 else False
            yellowFade = True if g == 255 and r == b == 0 else False
            redFade = True if r == g == 255 and b == 0 else False
        if purpleFade:
            b += 3
        if blueFade:
            r -= 3
        if tealFade:
            g += 3
        if greenFade:
            b -= 3
        if yellowFade:
            r += 3
        if redFade:
            g -= 3
        print(f'{r}, {g}, {b}')
        for num in range(i, 50+i):
            num = num if num < 299 else num - 300     
            pixels[num] = (int(r*(fade/5)), int(g*(fade/5)), int(b*(fade/5)))
            fade += 5/50
        pixels.show()
        if i != 299:
            i+=1
        else:
            i=0

        time.sleep(.01)

def Twinkle():
    i = 0
    pixels.fill((0,0,0))
    while i < (num_pixels/10):
        pixels[random.randint(0, (num_pixels-1))] = (255, 255, 255)
        i+=1
    pixels.show()
    time.sleep(1)

def fill(pissYellow = False, red = False, off = False, purple = False, green = False):
    if green == True:
        pixels.fill((0,255,0))
    if pissYellow == True:
        pixels.fill((255, 230, 0))
    if red == True:
        pixels.fill((255, 0, 0))
        if datetime.time(22) < datetime.datetime.now().time():
            pixels.brightness = 0.1
    if off == True:
        pixels.fill((0,0,0))
    if purple == True:
        pixels.fill((128,0,255))
    pixels.show()

def purpleTealFadeCycle():
    b = r = 255
    g = 0
    while True:
        if datetime.time(22) < datetime.datetime.now().time():
            break
        if r == g or r == b or b == g:
            blueFade = True if g == b == 255 and r == 0 else False
            purpleFade = True if b == 255 and g == r == 0 else False
            tealFade = True if b == r == 255 and g == 0 else False
        pixels.fill((r, g, b))
        pixels.show()
        if blueFade:
            g -= 1
        if purpleFade:
            r += 1
        if tealFade:
            g += 1
            r -= 1    

def fathersDayLED():
    # Green to Teal to Blue
    b = 0
    g = 255
    while True:
        if datetime.time(22) < datetime.datetime.now().time():
            break
        if b == g or b == 255 and g == 0 or g == 255 and b == 0:
            tealFade = True if g == 255 and b == 0 else False
            blueFade = True if g == b == 255 else False
            greenFade = True if b == 255 and g == 0 else False
        pixels.fill((0, g, b))
        pixels.show()
        if tealFade:
            b += 1
        if blueFade:
            g -= 1
        if greenFade:
            b -= 1
            g += 1
def mainLED(purpleTealCycleOn = False, colorTrailOn = False, twinkleOn = False, fillPissYellowOn = False, fillNightTimeRedOn = False, lightsOff = False, fillPurpleOn = False, purpleTealFadeOn = False, fillGreenOn = False, fathersDayOn = False):
    print(pixels.brightness)
    while True:
        if datetime.time(23,30) < datetime.datetime.now().time() or datetime.time(9) > datetime.datetime.now().time():
            fill(off=True)
        elif datetime.time(22) < datetime.datetime.now().time():
            fill(red=True)
        else:
            #strobe(0.1)
            if purpleTealCycleOn:
                purpleTealCycle(0.01)  # change purpleWheel to wheel for rainbow
            #fallColors()
            if colorTrailOn:
                ColorTrail()
            if twinkleOn:
                Twinkle()
            if fillPissYellowOn:
                fill(pissYellow=True)
            if fillNightTimeRedOn:
                fill(red=True)
            if lightsOff:
                fill(off=True)
            if fillPurpleOn:
                fill(purple=True)
            if purpleTealFadeOn:
                purpleTealFadeCycle()
            if fillGreenOn:
                fill(green=True)
            if fathersDayOn:
                fathersDayLED()
                
def TurnOnPurpleTealCycle():
    mainLED(purpleTealCycleOn = True)

def TurnOnColorTrail():
    mainLED(colorTrailOn = True)

def TurnOnTwinkle():
    mainLED(twinkleOn = True)

def TurnOnPissYellow():
    mainLED(fillPissYellowOn = True)

def TurnOnNightTimeRed():
    mainLED(fillNightTimeRedOn = True)

def TurnOffLights():
    mainLED(lightsOff = True)

def TurnOnPurple():
    mainLED(fillPurpleOn = True)

def TurnOnPurpleTealFade():
    mainLED(purpleTealFadeOn = True)

def TurnOnGreen():
    mainLED(fillGreenOn=True)

def BrightnessAdjustUp():
    pixels.brightness += 0.1
    print(pixels.brightness)

def BrightnessAdjustDown():
    pixels.brightness -= 0.1
    print(pixels.brightness)

def TurnOnFathersDay():
    mainLED(fathersDayOn=True)

master = tk.Tk()
master.title('Master Console')
master.geometry('600x100')

PurpleTealCycleButton = tk.Button(master, text="Purple Teal Cycle", bg="purple", command=TurnOnPurpleTealCycle)
PurpleTealCycleButton.grid(row=0, column=0)

ColorTrailButton = tk.Button(master, text="Color Trail", bg="pink", command=TurnOnColorTrail)
ColorTrailButton.grid(row=1, column=0)

TurnOnTwinkleButton = tk.Button(master, text="Twinkle", bg="white", command=TurnOnTwinkle)
TurnOnTwinkleButton.grid(row=2, column=0)

TurnOnPissYellowButton = tk.Button(master, text="Piss Yellow", bg="yellow", command=TurnOnPissYellow)
TurnOnPissYellowButton.grid(row=3, column=0)

TurnOffLEDButton = tk.Button(master, text="Off", bg="black", command=TurnOffLights)
TurnOffLEDButton.grid(row=0, column=1)

TurnOnNightTimeRedButton = tk.Button(master, text="Red", bg="red", command=TurnOnNightTimeRed)
TurnOnNightTimeRedButton.grid(row=1, column=1)

TurnOnPurpleButton = tk.Button(master, text="Purple", bg="purple", command=TurnOnPurple)
TurnOnPurpleButton.grid(row=2, column=1)

TurnOnPurpleTealFadeButton = tk.Button(master, text="Purple Teal Fade", bg="teal", command=TurnOnPurpleTealFade)
TurnOnPurpleTealFadeButton.grid(row=3, column=1)

TurnOnGreenButton = tk.Button(master, text="Green", bg="green", command=TurnOnGreen)
TurnOnGreenButton.grid(row=0, column=2)

BrightnessAdjustDownButton = tk.Button(master, text="Down", bg="white", command=BrightnessAdjustDown)
BrightnessAdjustDownButton.grid(row=2, column=2)

BrightnessAdjustUpButton = tk.Button(master, text='Up', bg='white', command=BrightnessAdjustUp)
BrightnessAdjustUpButton.grid(row=1, column=2)

FathersDayOnButton = tk.Button(master, text='Fathers Day', bg='teal', command=TurnOnFathersDay)
FathersDayOnButton.grid(row=2, column=2)

ExitButton = tk.Button(master, text="Exit the button", bg="red", command=sys.exit)
ExitButton.grid(row=3, column=3)

master.mainloop()

TurnOnPurpleTealFade()
