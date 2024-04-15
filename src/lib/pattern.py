# TODO: consider:
# - right now we have no context of the size of the strip, but do we care??
# - add in support for running an equation
# - add knowledge of when to write? auto write? write after full set? something else?
class Pattern:
    def __init__(self, name, frames):
        self._name = name
        self._frames = frames
        self._current_frame_index = 0

    def get_next_frame(self):
        frame = self._frames[self._current_frame_index]
        next_index = self._current_frame_index + 1

        if self._current_frame_index + 1 >= len(self._frames):
            next_index = 0

        self._current_frame_index = next_index
        return frame
