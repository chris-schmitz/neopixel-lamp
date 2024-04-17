# import unittest
from dataclasses import dataclass
from unittest import mock

import pytest
from unittest.mock import MagicMock


from src.lib.lamp_manager import LampManager
from src.lib.pattern import Pattern


def _build_lamp_manager(
    strip_constructor_mock,
    led_state,
    strip_length=3,
    initial_brightness=1.0,
    patterns=None,
    gpio_pin=1,
    auto_write=False,
):
    if patterns is None:
        patterns = []

    strip_constructor_mock.return_value = led_state

    return LampManager(
        strip_constructor=strip_constructor_mock,
        gpio_pin=gpio_pin,
        strip_length=strip_length,
        initial_brightness_level=initial_brightness,
        patterns=patterns,
        auto_write=auto_write,
    )


class TestSuite:

    def test_can_initialize_led_strip(self):
        strip_constructor = MagicMock()
        strip_length = 3
        led_state = [None] * 3
        strip_constructor.return_value = led_state
        gpio_pin = 1
        brightness_level = 1.0
        auto_write = False

        lamp = _build_lamp_manager(
            strip_constructor_mock=strip_constructor,
            led_state=led_state,
            gpio_pin=gpio_pin,
            strip_length=strip_length,
            auto_write=auto_write,
        )

        strip_constructor.assert_called_with(
            gpio_pin, strip_length, brightness_level, auto_write
        )

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
        strip_constructor = MagicMock()

        lamp = _build_lamp_manager(
            strip_constructor, led_strip, strip_length, patterns=patterns
        )

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
        strip_constructor = MagicMock()

        strip_length = 4
        led_strip = [None] * strip_length

        lamp = _build_lamp_manager(
            strip_constructor, led_strip, strip_length, patterns=patterns
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

    def test_can_update_brightness_level(self):
        pass
        # ? should the stepping up and down of the brightness level on button click be in this class or in the calling class?
