# TODO: consider:
# - right now we have no context of the size of the strip, but do we care??
# - add in support for running an equation
# - add knowledge of when to write? auto write? write after full set? something else?
import time


# * I haven't confirmed, but I'm pretty sure circuitpython doesn't support abstract base class
# * and I know for a fact it doesn't include typehinting  :'(, so I'm doing a super simple
# * informal interface here just to make sure our patterns all get the `get_next_frame` method.
class Pattern:

    def get_next_frame(self, current_millis):
        pass


class FramePattern(Pattern):
    def __init__(self, name, frames, interval, total_leds=None):
        self._name = name
        self._frames = frames
        self._total_leds = total_leds
        self._interval = interval
        self._current_position = 0
        self._last_interval_check = 0

    def _should_tick(self, current_millis):
        return current_millis - self._last_interval_check >= self._interval

    def get_next_frame(self, current_millis):
        if not self._should_tick(current_millis):
            return None

        frame = self._frames[self._current_position]
        next_index = self._current_position + 1

        if self._current_position + 1 >= len(self._frames):
            next_index = 0

        self._current_position = next_index
        self._last_interval_check = current_millis
        return frame


class CalcPattern(Pattern):
    def __init__(self, name, calc, total_leds, interval):
        self._name = name
        self._calc = calc
        self._total_leds = total_leds
        self._interval = interval
        self._current_position = 0
        self._last_interval_check = 0

    def _should_tick(self, current_millis):
        return current_millis - self._last_interval_check >= self._interval

    def get_next_frame(self, current_millis):
        if not self._should_tick(current_millis):
            return None

        self._last_interval_check = current_millis
        frame = [
            self._calc(self._current_position + index)
            for index in range(self._total_leds)
        ]

        self._current_position += self._total_leds
        if self._current_position > 255:
            self._current_position = 0

        return frame
