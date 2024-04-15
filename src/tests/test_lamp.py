# import unittest
from dataclasses import dataclass

import pytest
from unittest.mock import MagicMock

from src.lib.patternrunner import PatternRunner
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

        lamp = PatternRunner(led_strip, strip_length, patterns)

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

        lamp = PatternRunner(patterns)

        assert lamp.animate_next_frame() == [(1, 1, 1), (2, 2, 2), (3, 3, 3), (4, 4, 4)]
        assert lamp.animate_next_frame() == [(4, 4, 4), (5, 5, 5), (6, 6, 6), (7, 7, 7)]
        lamp.touch_trigger(1)
        assert lamp.animate_next_frame() == [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        assert lamp.animate_next_frame() == [(0, 0, 0), (0, 0, 0), (0, 0, 0)]
        lamp.touch_trigger(1)
        assert lamp.animate_next_frame() == [
            (8, 8, 8),
            (9, 9, 9),
            (10, 10, 10),
            (11, 11, 11),
        ]
        lamp.touch_trigger(1)
        assert lamp.animate_next_frame() == [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

    def test_touch_can_cycle_brightness(self):
        pass
        # ! brightness is set at strip object creation. we need to pass
        # ! the neopixel constructor in and recreate when brightness is changed
