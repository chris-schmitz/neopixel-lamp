# import unittest
import pytest

from lib.patterns import FramePattern, CalcPattern


class TestSuite:

    def test_frame_pattern_iteration(self):
        pattern = FramePattern(
            "test",
            [
                [(1, 1, 1), (2, 2, 2), (3, 3, 3)],
                [(4, 4, 4), (5, 5, 5), (6, 6, 6)],
            ],
            interval=1,
        )

        assert pattern.get_next_frame(0) is None
        assert pattern.get_next_frame(1) == [(1, 1, 1), (2, 2, 2), (3, 3, 3)]
        assert pattern.get_next_frame(2) == [(4, 4, 4), (5, 5, 5), (6, 6, 6)]
        assert pattern.get_next_frame(3) == [(1, 1, 1), (2, 2, 2), (3, 3, 3)]
        assert pattern.get_next_frame(4) == [(4, 4, 4), (5, 5, 5), (6, 6, 6)]

    def test_calc_pattern_can_manage_own_timing(self, wheel_function):
        def incrementer(start):
            return start + 1, start + 1, start + 1

        pattern = CalcPattern("timed", calc=incrementer, total_leds=2, interval=1)

        assert pattern.get_next_frame(0) is None
        assert pattern.get_next_frame(0.1) is None
        assert pattern.get_next_frame(1) == [(1, 1, 1), (2, 2, 2)]
        assert pattern.get_next_frame(2) == [(3, 3, 3), (4, 4, 4)]

    def test_calculation_pattern(self, wheel_function):

        pattern = CalcPattern("test", wheel_function, total_leds=4, interval=1)

        assert pattern.get_next_frame(0) is None
        assert pattern.get_next_frame(1) == [
            (0, 255, 0),
            (3, 252, 0),
            (6, 249, 0),
            (9, 246, 0),
        ]

        assert pattern.get_next_frame(2) == [
            (12, 243, 0),
            (15, 240, 0),
            (18, 237, 0),
            (21, 234, 0),
        ]

    @pytest.fixture
    def wheel_function(self):
        def wheel(pos):
            # Input a value 0 to 255 to get a color value.
            # The colours are a transition r - g - b - back to r.
            if pos < 0:
                return 0, 0, 0
            if pos > 255:
                return 0, 0, 0
            if pos < 85:
                return int(pos * 3), int(255 - (pos * 3)), 0
            elif pos < 170:
                pos -= 85
                return int(255 - pos * 3), 0, int(pos * 3)
            else:
                pos -= 170
                return 0, int(pos * 3), int(255 - pos * 3)

        return wheel
