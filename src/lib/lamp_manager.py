class LampManager:
    def __init__(self, led_strip, strip_length, patterns):
        # TODO: check-> can you get the strip length from `len` on the neopixel instance??
        self.led_strip = led_strip
        self.strip_length = strip_length
        self.patterns = patterns
        self._active_pattern_index = 0

    def touch_trigger(self, button_touched):
        match button_touched:
            case 1:
                self._active_pattern_index += 1
                if self._active_pattern_index >= len(self.patterns):
                    self._active_pattern_index = 0
            case 2:
                pass  # brightness

    def animate_next_frame(self):
        try:
            frame = self.patterns[self._active_pattern_index].get_next_frame()
            for index, pixel in enumerate(frame):
                self.led_strip[index] = pixel
        except IndexError as error:
            # TODO: switch out for playing default pattern instead
            print("Can't determine active pattern. Skipping...")
        except TypeError as error:
            # TODO: switch out for playing default pattern instead
            print("Can't determine active pattern. Skipping...")
