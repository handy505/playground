#!/usr/bin/env python3

class PVInverter(object):
    """ doctest here

    >>> pv = PVInverter()
    >>> pv.id
    1
    >>> pv.id = 2
    >>> pv.id
    2
    """
    def __init__(self):
        self._id = 1
        self._type = "unknow"

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, arg):
        self._id = arg

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    