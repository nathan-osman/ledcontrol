from os.path import join


class Device(object):
    """
    Represents an LED device
    """

    _CHANNELS = ['red', 'green', 'blue']

    def __init__(self, directory):
        """
        Initializes the device.
        """
        self._files = dict([(c, open(join(directory, c), 'r+')) for c in self._CHANNELS])

    def _read_value(self, channel):
        """
        Reads the value in the given color channel.
        """
        self._files[channel].seek(0)
        return int(self._files[channel].read(1))

    def _write_value(self, channel, value):
        """
        Writes the value to the given color channel.
        """
        self._files[channel].write(str(value))
        self._files[channel].flush()

    @property
    def color(self):
        """
        Returns the color of the device.
        """
        return [self._read_value(c) for c in self._CHANNELS]

    @color.setter
    def color(self, colors):
        """
        Sets the color of the device.
        """
        for c, v in zip(self._CHANNELS, colors):
            self._write_value(c, v)
