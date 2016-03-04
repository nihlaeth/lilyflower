"""Spanner objects."""
# pylint: disable=relative-import,too-few-public-methods
from errors import IllegalReuse


class Spanner(object):

    """
    Parent for spanner objects.

    A spanner has two parts, an open and a close. In this
    case, they are the same object. The first time __format__()
    is called, it displays the opening spanner, the second time,
    it displays the closing part. This ensures they are always
    closed properly, even if a sequense is reversed or sorted.
    """

    _num_displays = 0
    _delimiter_open = "("
    _delimiter_close = ")"
    _inline = True

    def __format__(self, _):
        """Return lilypond code."""
        if self._num_displays % 2 == 0:
            self._num_displays += 1
            return self._delimiter_open
        elif self._num_displays % 2 == 1:
            self._num_displays += 1
            return self._delimiter_close


class Slur(Spanner):

    """Slur spanner."""

    pass


class PhrasingSlur(Spanner):

    """Phrasing slur spanner."""

    _delimiter_open = "\\("
    _delimiter_close = "\\)"


class Beam(Spanner):

    """Manual beam spanner."""

    _delimiter_open = "["
    _delimiter_close = "]"
