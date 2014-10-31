from device import Device
from os import listdir
from os.path import isdir, join
from re import compile


class Enumerator(object):
    """
    Provides a means of enumerating devices
    """

    _PATH = '/sys/module/usbled/drivers/usb:usbled'
    _PATTERN = compile(r'\d+-[\d.]+:\d+.\d+')

    def __init__(self):
        """
        Initializes the enumerator by finding all devices
        """
        self.refresh()

    def __iter__(self):
        """
        Yields all available devices
        """
        for d in self._directories:
            yield Device(d)

    def _is_device(self, directory):
        """
        Returns true if the directory is for a device
        """
        return isdir(join(self._PATH, directory)) and self._PATTERN.match(directory)

    def refresh(self):
        """
        Refreshes the list of connected devices
        """
        try:
            self._directories = [join(self._PATH, d) for d in listdir(self._PATH) if self._is_device(d)]
        except OSError:
            self._directories = []
