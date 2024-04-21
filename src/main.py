from lib.lamp_manager import LampManager
from lib.pattern import Pattern
import board

# from digitalio import DigitalInOut, Direction, Pull
import touchio
import time

import neopixel

touch1 = touchio.TouchIn(board.D1)


#
#
# def main():
#     # *instantiate:
#     # - LED strip
#     # - touch buttons
#     # - Timer class (to write)
#     # - LampManager (rename pattern runner)
#     # - Patterns to use
#
patterns = [
    Pattern(
        "idle",
        [
            [
                (255, 0, 255),
                (25, 110, 55),
                (0, 30, 150),
                (255, 0, 255),
                (25, 110, 55),
                (0, 30, 150),
                (255, 0, 255),
                (25, 110, 55),
            ],
            [
                (25, 110, 55),
                (0, 30, 150),
                (255, 0, 255),
                (25, 110, 55),
                (0, 30, 150),
                (255, 0, 255),
                (25, 110, 55),
                (255, 0, 255),
            ],
            [
                (0, 30, 150),
                (255, 0, 255),
                (25, 110, 55),
                (0, 30, 150),
                (255, 0, 255),
                (25, 110, 55),
                (255, 0, 255),
                (25, 110, 55),
            ],
        ],
    ),
    Pattern(
        "solid blue",
        [
            [
                (0, 0, 255),
                (0, 0, 255),
                (0, 0, 255),
                (0, 0, 255),
                (0, 0, 255),
                (0, 0, 255),
                (0, 0, 255),
                (0, 0, 255),
            ]
        ],
    ),
]

lamp = LampManager(neopixel.NeoPixel, board.D0, 8, 0.1, patterns, False)

while True:
    time.sleep(0.3)
    lamp.animate_next_frame()

    if touch1.value:
        lamp.touch_trigger(1)
