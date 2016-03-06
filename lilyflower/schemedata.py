"""Scheme datatypes."""
# pylint: disable=super-init-not-called
import collections
import re
from lilyflower.errors import InvalidArgument


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


class Boolean(SchemeData):

    """Boolean value."""

    def __init__(self, data):
        """Check if bool."""
        if not isinstance(data, bool):
            raise InvalidArgument("%r is not a bool." % data)
        if data:
            self._data = "#t"
        else:
            self._data = "#f"

    def __format__(self, _):
        """Return lilypond cgde."""
        return "%s%s" % (self._start_symbol, self._data)


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
        if not isinstance(data, float) and not isinstance(data, int):
            raise InvalidArgument("%r is not a float." % data)
        elif data < 0:
            raise InvalidArgument("%d is smaller than zero." % data)
        else:
            self._data = data


class SignedFloat(SchemeData):

    """Signed float."""

    def __init__(self, data):
        """Make sure it's a signed float."""
        if not isinstance(data, float) and not isinstance(data, int):
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


class Color(SchemeData):

    """Color." representation in scheme."""

    def __init__(self, data):
        """Determine if color is valid and wihat type it is."""
        normal_colors = [
            'black',
            'blue',
            'grey',
            'darkcyan',
            'white',
            'cyan',
            'darkred',
            'darkmagenta',
            'red',
            'magenta',
            'darkgreen',
            'darkyellow',
            'green',
            'yellow',
            'darkblue']
        x11_colors_simple = [
            'snow',
            'GhostWhite', 'ghost white',
            'WhiteSmoke', 'white smoke',
            'gainsboro',
            'FloralWhite', 'floral white',
            'OldLace', 'old lace',
            'linen',
            'AntiqueWhite', 'antique white',
            'PapayaWhip', 'papaya whip',
            'BlanchedAlmond', 'blanched almond',
            'bisque',
            'PeachPuff', 'peach puff',
            'NavajoWhite', 'navajo white',
            'moccasin',
            'cornsilk',
            'ivory',
            'LemonChiffon', 'lemon chiffon',
            'seashell',
            'honeydew',
            'MintCream', 'mint cream',
            'azure',
            'AliceBlue', 'alice blue',
            'lavender',
            'LavenderBlush', 'lavender blush',
            'MistyRose', 'misty rose',
            'white',
            'black',
            'DarkSlateGrey', 'dark slate grey',
            'DimGrey', 'dim grey',
            'SlateGrey', 'slate grey',
            'LightSlateGrey', 'light slate grey',
            'grey',
            'LightGrey', 'light grey',
            'MidnightBlue', 'midnight blue',
            'navy',
            'NavyBlue', 'navy blue',
            'CornflowerBlue', 'cornflower blue',
            'DarkSlateBlue', 'dark slate blue',
            'SlateBlue', 'slate blue',
            'MediumSlateBlue', 'medium slate blue',
            'LightSlateBlue', 'light slate blue',
            'MediumBlue', 'medium blue',
            'RoyalBlue', 'royal blue',
            'blue',
            'DodgerBlue', 'dodger blue',
            'DeepSkyBlue', 'deep sky blue',
            'SkyBlue', 'sky blue',
            'LightSkyBlue', 'light sky blue',
            'SteelBlue', 'steel blue',
            'LightSteelBlue', 'light steel blue',
            'LightBlue', 'light blue',
            'PowderBlue', 'powder blue',
            'PaleTurquoise', 'pale turquoise',
            'DarkTurquoise', 'dark turquoise',
            'MediumTurquoise', 'medium turquoise',
            'turquoise',
            'cyan',
            'LightCyan', 'light cyan',
            'CadetBlue', 'cadet blue',
            'MediumAquamarine', 'medium aquamarine',
            'aquamarine',
            'DarkGreen', 'dark green',
            'DarkOliveGreen', 'dark olive green',
            'DarkSeaGreen', 'dark sea green',
            'SeaGreen', 'sea green',
            'MediumSeaGreen', 'medium sea green',
            'LightSeaGreen', 'light sea green',
            'PaleGreen', 'pale green',
            'SpringGreen', 'spring green',
            'LawnGreen', 'lawn green',
            'green',
            'chartreuse',
            'MediumSpringGreen', 'medium spring green',
            'GreenYellow', 'green yellow',
            'LimeGreen', 'lime green',
            'YellowGreen', 'yellow green',
            'ForestGreen', 'forest green',
            'OliveDrab', 'olive drab',
            'DarkKhaki', 'dark khaki',
            'khaki',
            'PaleGoldenrod', 'pale goldenrod',
            'LightGoldenrodYellow', 'light goldenrod yellow',
            'LightYellow', 'light yellow',
            'yellow',
            'gold',
            'LightGoldenrod', 'light goldenrod',
            'goldenrod',
            'DarkGoldenrod', 'dark goldenrod',
            'RosyBrown', 'rosy brown',
            'IndianRed', 'indian red',
            'SaddleBrown', 'saddle brown',
            'sienna',
            'peru',
            'burlywood',
            'beige',
            'wheat',
            'SandyBrown', 'sandy brown',
            'tan',
            'chocolate',
            'firebrick',
            'brown',
            'DarkSalmon', 'dark salmon',
            'salmon',
            'LightSalmon', 'light salmon',
            'orange',
            'DarkOrange', 'dark orange',
            'coral',
            'LightCoral', 'light coral',
            'tomato',
            'OrangeRed', 'orange red',
            'red',
            'HotPink', 'hot pink',
            'DeepPink', 'deep pink',
            'pink',
            'LightPink', 'light pink',
            'PaleVioletRed', 'pale violet red',
            'maroon',
            'MediumVioletRed', 'medium violet red',
            'VioletRed', 'violet red',
            'magenta',
            'violet',
            'plum',
            'orchid',
            'MediumOrchid', 'medium orchid',
            'DarkOrchid', 'dark orchid',
            'DarkViolet', 'dark violet',
            'BlueViolet', 'blue violet',
            'purple',
            'MediumPurple', 'medium purple',
            'thistle',
            'DarkGrey', 'dark grey',
            'DarkBlue', 'dark blue',
            'DarkCyan', 'dark cyan',
            'DarkMagenta', 'dark magenta',
            'DarkRed', 'dark red',
            'LightGreen', 'light green']

        numbered_colors = [
            'snow', 'seashell', 'AntiqueWhite', 'bisque', 'PeachPuff',
            'NavajoWhite', 'LemonChiffon', 'cornsilk', 'ivory', 'honeydew',
            'LavenderBlush', 'MistyRose', 'azure', 'SlateBlue', 'RoyalBlue',
            'blue', 'DodgerBlue', 'SteelBlue', 'DeepSkyBlue', 'SkyBlue',
            'LightSkyBlue', 'LightSteelBlue', 'LightBlue', 'LightCyan',
            'CadetBlue', 'turquoise', 'cyan', 'aquamarine', 'DarkSeaGreen',
            'SeaGreen', 'PaleGreen', 'SpringGreen', 'green', 'chartreuse',
            'OliveDrab', 'DarkOliveGreen', 'khaki', 'LightGoldenrod',
            'yellow', 'gold', 'goldenrod', 'DarkGoldenrod', 'RosyBrown',
            'IndianRed', 'sienna', 'burlywood', 'wheat', 'tan',
            'chocolate', 'firebrick', 'brown', 'salmon', 'LightSalmon',
            'orange', 'DarkOrange', 'coral', 'tomato', 'OrangeRed',
            'red', 'DeepPink', 'HotPink', 'pink', 'LightPink',
            'PaleVioletRed', 'maroon', 'VioletRed', 'magenta', 'orchid',
            'plum', 'MediumOrchid', 'DarkOrchid', 'purple',
            'MediumPurple', 'thistle', 'LightYellow', 'PaleTurquoise']

        x11_colors_numbered = [
            a + str(b) for a in numbered_colors for b in range(1, 5)]

        if data in normal_colors:
            self._data = data
        elif re.match("^grey[0-9]+$", data):
            self._data = "(x11-color \"%s\")" % data
        elif data in x11_colors_simple or data in x11_colors_numbered:
            self._data = "(x11-color \"%s\")" % data
        else:
            raise InvalidArgument("%r is not a valid color.")

    def __format__(self, _):
        """Return lilypond code."""
        return "%s%s" % (self._start_symbol, self._data)
