from colorsys import yiq_to_rgb, rgb_to_yiq
from math import cos, pi
from os.path import join
from time import sleep


class Device(object):
    """
    Represents an LED device.
    """

    _CHANNELS = ['red', 'green', 'blue']
    _TICK = 30**-1
    _PREDEFINED = {
        'white': (1, 1, 1),
        'silver': (0.75, 0.75, 0.75),
        'grey': (0.5, 0.5, 0.5),
        'black': (0, 0, 0),
        'red': (1, 0, 0),
        'maroon': (0.5, 0, 0),
        'yellow': (1, 1, 0),
        'olive': (0.5, 0.5, 0),
        'lime': (0, 1, 0),
        'green': (0, 0.5, 0),
        'aqua': (0, 1, 1),
        'teal': (0, 0.5, 0.5),
        'blue': (0, 0, 1),
        'navy': (0, 0, 0.5),
        'fuchsia': (1, 0, 1),
        'purple': (0.5, 0, 0.5),
    }

    def __init__(self, directory):
        """
        Initializes the device.
        """
        self._files = dict([(c, open(join(directory, c), 'r+')) for c in self._CHANNELS])

    def _interpolate(self, cur, start, end):
        """
        Interpolate from start to end.
        """
        v = 0.5 - cos(pi * cur) / 2
        return start - v * (start - end)

    def _read_value(self, channel):
        """
        Reads the value in the given color channel.
        """
        self._files[channel].seek(0)
        return int(self._files[channel].read()) / 64.0

    def _translate(self, color):
        """
        Translate the input to a tuple if necessary.
        """
        if isinstance(color, basestring):
            color = self._PREDEFINED.get(color, (0, 0, 0))
        return color

    def _write_value(self, channel, value):
        """
        Writes the value to the given color channel.
        """
        value = min(64, max(0, int(value * 64)))
        self._files[channel].write(str(value))
        self._files[channel].flush()

    @property
    def color(self):
        """
        Returns the color of the device.
        """
        return [self._read_value(c) for c in self._CHANNELS]

    @color.setter
    def color(self, color):
        """
        Sets the color of the device.
        """
        for c, v in zip(self._CHANNELS, self._translate(color)):
            self._write_value(c, v)

    def interpolate(self, start_color, end_color, duration=0.5):
        """
        Interpolate between two colors.
        """
        colors = zip(
            rgb_to_yiq(*self._translate(start_color)),
            rgb_to_yiq(*self._translate(end_color)),
        )
        i, tick = 0, (duration**-1 * self._TICK)
        while i < 1:
            self.color = yiq_to_rgb(*map(lambda x: self._interpolate(i, *x), colors))
            i += tick
            sleep(self._TICK)
        self.color = end_color

    def pulse(self, color, count=1, interval=1):
        """
        Pulse between black and the specified color.
        """
        for i in xrange(count):
            self.interpolate('black', color, interval / 2.0)
            self.interpolate(color, 'black', interval / 2.0)
