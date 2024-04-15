# import unittest
from dataclasses import dataclass

import pytest
from unittest.mock import MagicMock

from src.lib.lamp_manager import LampManager
from src.lib.pattern import Pattern


class TestSuite:
    def test_touch_can_set_active_pattern(self):
        patterns = [
            Pattern(
                "pattern 1",
                [
                    [(1, 1, 1), (2, 2, 2), (3, 3, 3)],
                    [(4, 4, 4), (5, 5, 5), (6, 6, 6)],
                ],
            )
        ]
        strip_length = 3
        led_strip = [None] * strip_length

        lamp = LampManager(led_strip, strip_length, patterns)

        lamp.animate_next_frame()
        assert led_strip[0] == (1, 1, 1)
        assert led_strip[1] == (2, 2, 2)
        assert led_strip[2] == (3, 3, 3)
        lamp.animate_next_frame()
        assert led_strip[0] == (4, 4, 4)
        assert led_strip[1] == (5, 5, 5)
        assert led_strip[2] == (6, 6, 6)
        lamp.animate_next_frame()
        assert led_strip[0] == (1, 1, 1)
        assert led_strip[1] == (2, 2, 2)
        assert led_strip[2] == (3, 3, 3)
        lamp.animate_next_frame()
        assert led_strip[0] == (4, 4, 4)
        assert led_strip[1] == (5, 5, 5)
        assert led_strip[2] == (6, 6, 6)

    # TODO: fix this test to work with injected LED strip
    def test_touching_buttons_can_switch_between_patterns(self):
        patterns = [
            Pattern(
                "pattern 1",
                [
                    [(1, 1, 1), (2, 2, 2), (3, 3, 3), (4, 4, 4)],
                    [(4, 4, 4), (5, 5, 5), (6, 6, 6), (7, 7, 7)],
                    [(8, 8, 8), (9, 9, 9), (10, 10, 10), (11, 11, 11)],
                ],
            ),
            Pattern(
                "pattern 2",
                [
                    [(255, 0, 0), (0, 255, 0), (0, 0, 255)],
                    [(0, 0, 0), (0, 0, 0), (0, 0, 0)],
                ],
            ),
        ]
        strip_length = 4
        led_strip = [None] * strip_length

        lamp = LampManager(
            led_strip=led_strip, strip_length=strip_length, patterns=patterns
        )

        lamp.animate_next_frame()
        assert led_strip[0] == (1, 1, 1)
        assert led_strip[1] == (2, 2, 2)
        assert led_strip[2] == (3, 3, 3)
        assert led_strip[3] == (4, 4, 4)
        lamp.animate_next_frame()
        assert led_strip[0] == (4, 4, 4)
        assert led_strip[1] == (5, 5, 5)
        assert led_strip[2] == (6, 6, 6)
        assert led_strip[3] == (7, 7, 7)

        lamp.touch_trigger(1)
        lamp.animate_next_frame()
        assert led_strip[0] == (255, 0, 0)
        assert led_strip[1] == (0, 255, 0)
        assert led_strip[2] == (0, 0, 255)
        # !! Note that I'm not blanking out previous cells if you don't account for it in your pattern!
        # !! That's your responsibility (at the moment, though I may bake that into the pattern class post mvp)
        assert led_strip[3] == (7, 7, 7)
        lamp.animate_next_frame()
        assert led_strip[0] == (0, 0, 0)
        assert led_strip[1] == (0, 0, 0)
        assert led_strip[2] == (0, 0, 0)
        assert led_strip[3] == (7, 7, 7)

        lamp.touch_trigger(1)
        lamp.animate_next_frame()
        assert led_strip[0] == (8, 8, 8)
        assert led_strip[1] == (9, 9, 9)
        assert led_strip[2] == (10, 10, 10)
        assert led_strip[3] == (11, 11, 11)

        lamp.touch_trigger(1)
        lamp.animate_next_frame()
        assert led_strip[0] == (255, 0, 0)
        assert led_strip[1] == (0, 255, 0)
        assert led_strip[2] == (0, 0, 255)
        assert led_strip[3] == (11, 11, 11)

    def test_touch_can_cycle_brightness(self):
        pass
        # ! brightness is set at strip object creation. we need to pass
        # ! the neopixel constructor in and recreate when brightness is changed
