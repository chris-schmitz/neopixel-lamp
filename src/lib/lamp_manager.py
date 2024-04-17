class LampManager:
    def __init__(
        self,
        strip_constructor,
        gpio_pin,
        strip_length,
        initial_brightness_level,
        patterns,
        auto_write=False,
    ):
        self.strip_constructor = strip_constructor
        self.gpio_pin = gpio_pin
        self.led_strip = None
        self.brightness_level = initial_brightness_level
        self.strip_length = strip_length
        self.auto_write = auto_write
        self._initialize_led_strip()

        self.patterns = patterns
        self._active_pattern_index = 0

    def _initialize_led_strip(self):
        self.led_strip = self.strip_constructor(
            self.gpio_pin, self.strip_length, self.brightness_level, self.auto_write
        )

    # def set_brightness_level(self, brightness_level):
    #     self.led_strip = self.strip_constructor(
    #         self.gpio_pin, self.strip_length, brightness_level, False
    #     )

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
