# Trinket IO demo
# Welcome to CircuitPython 3.1.1 :)

import board
from digitalio import DigitalInOut, Direction, Pull
import touchio
import time
import neopixel



touchBoard = DigitalInOut(board.D2)
touchBoard.direction = Direction.INPUT
touchBoard.pull = Pull.UP

# Facepalm
# Capacitive touch on D3
touch1 = touchio.TouchIn(board.D3)
touch2 = touchio.TouchIn(board.D4)
touch3 = touchio.TouchIn(board.D1)

# NeoPixel strip (of 16 LEDs) connected on D4
NUMPIXELS = 16
neopixels = neopixel.NeoPixel(board.D0, NUMPIXELS, brightness=0.2, auto_write=False)


######################### HELPERS ##############################


# Helper to give us a nice color swirl
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if (pos < 0):
        return (0, 0, 0)
    if (pos > 255):
        return (0, 0, 0)
    if (pos < 85):
        return (int(pos * 3), int(255 - (pos*3)), 0)
    elif (pos < 170):
        pos -= 85
        return (int(255 - pos*3), 0, int(pos*3))
    else:
        pos -= 170
        return (0, int(pos*3), int(255 - pos*3))

######################### MAIN LOOP ##############################

def up_and_down_leds():
    for p in range(NUMPIXELS):
        idx = int ((p * 256 / NUMPIXELS) + i)
        neopixels[p] = wheel(idx & 255)
        neopixels.show()
        time.sleep(0.025)
    for p in range(NUMPIXELS):
        neopixels[NUMPIXELS - p - 1] = (0,0,0)
        neopixels.show()
        time.sleep(0.025)
    # neopixels.show()

def blink_leds():
    for round in range(0, 4):
      for p in range(NUMPIXELS):
          neopixels[p] = (255,0,255)
      neopixels.show()
      time.sleep(0.025)
      for p in range(NUMPIXELS):
          neopixels[p] = (0,0,0)

def rainbow_swirl():
    i = 0
    for round in range(0, 4):
      for p in range(NUMPIXELS):
          idx = int ((p * 256 / NUMPIXELS) + i)
          neopixels[p] = wheel(idx & 255)
      neopixels.show()
      time.sleep(0.025)

i = 0
check_interval = 0.01
last_check = 0

while True:
    if(time.monotonic() - check_interval > last_check):
        i += 1
        last_check = time.monotonic()
        # if touchBoard.value:
        #     print("---> board touch")
        #     swirl_leds()
        
        if touch1.value:
            print("===> pin 1 touch")
            up_and_down_leds()

        if touch2.value:
            print("===> pin 2 touch")
            blink_leds()

        if touch3.value:
            print("===> pin 3 touch")
            rainbow_swirl()
    else:
      for p in range(NUMPIXELS):
        neopixels[NUMPIXELS - p - 1] = (0,0,0)
      neopixels.show()
      time.sleep(0.025)