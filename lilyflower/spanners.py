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

    num_displays = 0
    delimiter_open = "("
    delimiter_close = ")"
    inline = True

    def __format__(self, _):
        """Return lilypond code."""
        if self.num_displays % 2 == 0:
            self.num_displays += 1
            return self.delimiter_open
        elif self.num_displays % 2 == 1:
            self.num_displays += 1
            return self.delimiter_close


class Slur(Spanner):

    """Slur spanner."""

    pass


class PhrasingSlur(Spanner):

    """Phrasing slur spanner."""

    delimiter_open = "\\("
    delimiter_cloe = "\\)"


class Beam(Spanner):

    """Manual beam spanner."""

    delimiter_open = "["
    delimiter_close = "]"
