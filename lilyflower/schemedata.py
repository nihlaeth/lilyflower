"""Scheme datatypes."""
# pylint: disable=relative-import,too-few-public-methods,super-init-not-called
import collections
from errors import InvalidArgument


class SchemeData(object):

    """Scheme data."""

    start_symbol = "#"
    inline = True

    def __init__(self, data):
        """Convert python data to scheme data."""
        self.data = data

    def nested(self):
        """Data for nested use (used by compound SchemeData objects)."""
        return self.data

    def __format__(self, _):
        """Return lilypond code."""
        return "%s%r" % (self.start_symbol, self.data)


class UnsignedInt(SchemeData):

    """Unsigned integer."""

    def __init__(self, data):
        """Make sure it's an unsigned int."""
        if not isinstance(data, int):
            raise InvalidArgument("%r is not an integer." % data)
        elif data < 0:
            raise InvalidArgument("%d is smaller than zero." % data)
        else:
            self.data = data


class SignedInt(SchemeData):

    """Signed integer."""

    def __init__(self, data):
        """Make sure it's an integer."""
        if not isinstance(data, int):
            raise InvalidArgument("%r is not an integer." % data)
        else:
            self.data = data


class UnsignedFloat(SchemeData):

    """Unsigned float."""

    def __init__(self, data):
        """Make sure it's an unsigned float."""
        if not isinstance(data, float):
            raise InvalidArgument("%r is not a float." % data)
        elif data < 0:
            raise InvalidArgument("%d is smaller than zero." % data)
        else:
            self.data = data


class SignedFloat(SchemeData):

    """Signed float."""

    def __init__(self, data):
        """Make sure it's a signed float."""
        if not isinstance(data, float):
            raise InvalidArgument("%r is not a float." % data)
        else:
            self.data = data


class String(SchemeData):

    """String."""

    def __init__(self, data):
        """Make sure it's a string."""
        self.data = str(data)


class Direction(SchemeData):

    """Not an official Scheme data type, but used a lot in lilypond."""

    def __init__(self, data):
        """Check it it's a valid direction."""
        if data in ["up", "Up", "UP"]:
            self.data = "UP"
        elif data in ["down", "Down", "DOWN"]:
            self.data = "DOWN"
        elif data in ["center", "Center", "CENTER"]:
            self.data = "CENTER"
        else:
            raise InvalidArgument("Expected up, down or center, not %r" % data)

    def nested(self):
        """Data for nested use (used by compound SchemeData objects)."""
        return self.data

    def __format__(self, _):
        """Return lilypond code."""
        return "%s%s" % (self.start_symbol, self.data)


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
            self.data = data

    def nested(self):
        """Data for nested use (used by compound SchemeData objects)."""
        return "(%r . %r)" % (self.data[0].nested(), self.data[1].nested())

    def __format__(self, _):
        """Return lilypond code."""
        return "%s'(%r . %r)" % (
            self.start_symbol,
            str(self.data[0]),
            str(self.data[1]))


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
        self.data = data

    def nested(self):
        """Data for nested use (used by compound SchemeData objects)."""
        return "(%s)" % " ".join("%r" % item.nested() for item in self.data)

    def __format__(self, _):
        """Return lilypond code."""
        return "%s'(%s)" % (
            self.start_symbol,
            " ".join("%r" % item.nested() for item in self.data))


class AssociationList(List):

    """Association list."""

    def __init__(self, data):
        """Make sure every item is a pair."""
        List.__init__(self, data)
        for item in data:
            if not isinstance(item, Pair):
                raise InvalidArgument("%r is not a Pair object." % item)
