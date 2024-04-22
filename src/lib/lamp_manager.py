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
        self._strip_constructor = strip_constructor
        self._gpio_pin = gpio_pin
        self._led_strip = None
        self._brightness_level = initial_brightness_level
        self._strip_length = strip_length
        self._auto_write = auto_write
        self._initialize_led_strip()

        self._patterns = patterns
        self._active_pattern_index = 0

    def touch_trigger(self, button_touched):
        print("touched: ")
        print(button_touched)
        if button_touched == 1:
            self._increment_active_pattern_index()
        elif button_touched == 2:
            self._step_down_brightness_level()
        else:
            raise ValueError("invalid touch value: " + str(button_touched))

    def animate_next_frame(self):
        try:
            frame = self._patterns[self._active_pattern_index].get_next_frame()
            print(frame)
            for index, pixel in enumerate(frame):
                self._led_strip[index] = pixel
            self._led_strip.show()
        except IndexError as error:
            # TODO: talk with andrew, how would I test for this?
            # * the way this class is set up without reaching in to a private property
            # * there actually isn't a way to induce these exceptions, but I don't want
            # * to not have the excepts b/c the way this particular method is structured
            # * in theory it _could_ throw an exception. So do I write a test that takes
            # * advantage of the "nothing's really private" aspect of python to force a test
            # * or do I do something else??
            print("Can't determine active pattern. Skipping...")
        except TypeError as error:
            # TODO: switch out for playing default pattern instead
            print("Can't determine active pattern. Skipping...")

    def _initialize_led_strip(self):
        self._led_strip = self._strip_constructor(
            self._gpio_pin,
            self._strip_length,
            brightness=self._brightness_level,
            auto_write=self._auto_write,
        )

    def _set_brightness_level(self, brightness_level):
        self._brightness_level = brightness_level
        # TODO: Figure out how to assert the deinit call this in the test.
        # ? https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel/blob/310621f32839b73f892b227650c5d002a310e7c5/neopixel.py#L144
        # * I think we need to make a magic mock that uses the getattribute and set attribute magic methods
        # self._led_strip.deinit()
        self._led_strip = self._strip_constructor(
            self._gpio_pin,
            self._strip_length,
            brightness=brightness_level,
            auto_write=False,
        )

    def _step_down_brightness_level(self):
        new_level = round(self._brightness_level - 0.1, 1)
        if new_level < 0:
            new_level = 1.0
        self._set_brightness_level(new_level)

    def _increment_active_pattern_index(self):
        self._active_pattern_index += 1
        if self._active_pattern_index >= len(self._patterns):
            self._active_pattern_index = 0
