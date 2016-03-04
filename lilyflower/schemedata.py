"""Scheme datatypes."""
# pylint: disable=relative-import,too-few-public-methods,super-init-not-called
import collections
from errors import InvalidArgument


class SchemeData(object):

    """Scheme data."""

    _start_symbol = "#"
    _inline = True

    def __init__(self, data):
        """Convert python data to scheme data."""
        self._data = data

    def nested(self):
        """Data for nested use (used by compound SchemeData objects)."""
        return self._data

    def __format__(self, _):
        """Return lilypond code."""
        return "%s%r" % (self._start_symbol, self._data)


class UnsignedInt(SchemeData):

    """Unsigned integer."""

    def __init__(self, data):
        """Make sure it's an unsigned int."""
        if not isinstance(data, int):
            raise InvalidArgument("%r is not an integer." % data)
        elif data < 0:
            raise InvalidArgument("%d is smaller than zero." % data)
        else:
            self._data = data


class SignedInt(SchemeData):

    """Signed integer."""

    def __init__(self, data):
        """Make sure it's an integer."""
        if not isinstance(data, int):
            raise InvalidArgument("%r is not an integer." % data)
        else:
            self._data = data


class UnsignedFloat(SchemeData):

    """Unsigned float."""

    def __init__(self, data):
        """Make sure it's an unsigned float."""
        if not isinstance(data, float):
            raise InvalidArgument("%r is not a float." % data)
        elif data < 0:
            raise InvalidArgument("%d is smaller than zero." % data)
        else:
            self._data = data


class SignedFloat(SchemeData):

    """Signed float."""

    def __init__(self, data):
        """Make sure it's a signed float."""
        if not isinstance(data, float):
            raise InvalidArgument("%r is not a float." % data)
        else:
            self._data = data


class String(SchemeData):

    """String."""

    def __init__(self, data):
        """Make sure it's a string."""
        self._data = str(data)


class Direction(SignedFloat):

    """Not an official Scheme data type, but used a lot in lilypond."""

    def __init__(self, data):
        """Check it it's a valid direction."""
        if data in ["up", "Up", "UP"]:
            self._data = "UP"
        elif data in ["down", "Down", "DOWN"]:
            self._data = "DOWN"
        elif data in ["center", "Center", "CENTER"]:
            self._data = "CENTER"
        else:
            raise InvalidArgument("Expected up, down or center, not %r" % data)

    def nested(self):
        """Data for nested use (used by compound SchemeData objects)."""
        return self._data

    def __format__(self, _):
        """Return lilypond code."""
        return "%s%s" % (self._start_symbol, self._data)


class Axis(SignedInt):

    """Not an official Scheme data type, but used a lot in lilypond."""

    def __init__(self, data):
        """Check if it's a valid axis."""
        if data in ["x", "X"]:
            self._data = "X"
        elif data in ["y", "Y"]:
            self._data = "Y"
        else:
            raise InvalidArgument("Expected X or Y, not %r" % data)

    def nested(self):
        """Data for nested use (used by compound SchemeData objects)."""
        return self._data

    def __format__(self, _):
        """Return lilypond code."""
        return "%s%s" % (self._start_symbol, self._data)


class Pair(SchemeData):

    """Pair."""

    def __init__(self, data):
        """Make sure it's a sequence of length two."""
        if isinstance(data, basestring) or \
                not isinstance(data, collections.Sequence):
            raise InvalidArgument("%r is not a sequence." % data)
        elif len(data) != 2:
            raise InvalidArgument("%r does not have a length of 2." % data)
        elif not isinstance(data[0], SchemeData):
            raise InvalidArgument("%r is not a SchemeData object." % data)
        elif not isinstance(data[1], SchemeData):
            raise InvalidArgument("%r is not a SchemeData object." % data)
        else:
            self._data = data

    def nested(self):
        """Data for nested use (used by compound SchemeData objects)."""
        return "(%r . %r)" % (self._data[0].nested(), self._data[1].nested())

    def __format__(self, _):
        """Return lilypond code."""
        return "%s'(%r . %r)" % (
            self._start_symbol,
            str(self._data[0]),
            str(self._data[1]))


class List(SchemeData):

    """List."""

    def __init__(self, data):
        """Make sure it's a sequence."""
        if isinstance(data, basestring) or \
                not isinstance(data, collections.Sequence):
            raise InvalidArgument("%r is not a sequence." % data)
        for item in data:
            if not isinstance(item, SchemeData):
                raise InvalidArgument("%r is not a SchemeData object." % item)
        self._data = data

    def nested(self):
        """Data for nested use (used by compound SchemeData objects)."""
        return "(%s)" % " ".join("%r" % item.nested() for item in self._data)

    def __format__(self, _):
        """Return lilypond code."""
        return "%s'(%s)" % (
            self._start_symbol,
            " ".join("%r" % item.nested() for item in self._data))


class AssociationList(List):

    """Association list."""

    def __init__(self, data):
        """Make sure every item is a pair."""
        List.__init__(self, data)
        for item in data:
            if not isinstance(item, Pair):
                raise InvalidArgument("%r is not a Pair object." % item)
