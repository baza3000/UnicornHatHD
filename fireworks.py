# This example gist makes fireworks appear on the Raspberry Pi Unicorn Hat HD.
import unicornhathd as unicorn

from time import sleep
from random import randint
import threading

unicorn.rotation(90)

DECAY = 0.7 # Colour decay of firework head.
SPEED = 0.1 # Speed of firework explosion.
DISPLAY_SPEED = 0.5 # Speed of firework launches.
SIZE = 7 # Size of firework head, should be between 1 and 7.

unicorn.clear()

def firework_head(i, j, r, g, b):
    # Make the firework explody bit.
    # Expand 7 pixels out by SIZE across the sense hat, using DECAY to fade the firework head.
    for x in range(0, SIZE):
        if(i-x >= 0): unicorn.set_pixel(i-x, j, r, g, b)
        if(j-x >= 0): unicorn.set_pixel(i, j-x, r, g, b)
        if(i+x <= 7): unicorn.set_pixel(i+x, j, r, g, b)
        if(j+x <= 7):unicorn.set_pixel(i, j+x, r, g, b)
        sleep(SPEED)
        # Tidy the head at each step.
        tidy_head(i, j, x)
        # Fade the head colour if requested.
        r = int(r * DECAY)
        g = int(g * DECAY)
        b = int(b * DECAY)
        unicorn.show()

def firework_tail(i, j, r, g, b):
    # Make the firework fiery tail.
    for x in range(15, j, -1):
        unicorn.set_pixel(i, x, r, g, b)
        sleep(SPEED)
    # Tidy the tail once the tail has gone all the way.
    tidy_tail(i, j)
    unicorn.show()

def tidy_tail(i, j):
    # Tidy up the tail.
    for x in range(15, j, -1):
        unicorn.set_pixel(i, x, 0, 0, 0)
    unicorn.show()   

def tidy_head(i, j, x):
    # Tidy the head of the firework.
    if(i-x >= 0): unicorn.set_pixel(i-x, j, 0, 0, 0)
    if(j-x >= 0): unicorn.set_pixel(i, j-x, 0, 0, 0)
    if(i+x <= 7): unicorn.set_pixel(i+x, j, 0, 0, 0)
    if(j+x <= 7): unicorn.set_pixel(i, j+x, 0, 0, 0)
    unicorn.show()

def firework():
    # Make a firework at a random point on the sense hat.
    i = randint(0, 15)
    j = randint(0, 4) # Not 7 so our fireworks will always be at least halfway.
    # Pick a random brightish colour for the firework. Also this allows for colour decay if using DECAY.
    r = randint(100, 255)
    g = randint(100, 255)
    b = randint(100, 255)
    # Tails will be orange, because that's what colour they are.
    firework_tail(i, j, 255, 100, 0)
    firework_head(i, j, r, g, b)
    unicorn.show()
    
try:
    while True:
        # Set up threading of firework so that multiple fireworks can be displayed at the same time.
        thread = threading.Thread(target=firework)
        thread.start()
        # Speed of firework display.
        sleep(DISPLAY_SPEED)
except KeyboardInterrupt:
    # Clear the sense hat when the display is over.
    unicorn.clear()

