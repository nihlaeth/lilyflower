"""Container derived classes."""
import datetime

from container import Container
from errors import InvalidArgument


class LilyFile(Container):

    """Container for a single lilypond file."""

    def __init__(self, contents, arguments=None):
        """Set delimiters as empty and make sure there are no arguments."""
        Container.__init__(self, contents, arguments)
        if len(self.arguments) > 0:
            raise InvalidArgument("No arguments allowed!")
        self.delimiter_pre = ""
        self.delimiter_post = ""

    def __format__(self, _):
        """Return lilypond code."""
        result = "%% Created with lilyflower at %s\n\n" % datetime.datetime.now()
        for item in self.container:
            if isinstance(item, Container):
                result += format(item)
            else:
                result += "%s " % format(item)
        return result


class Book(Container):

    """Book container."""

    def __init__(self, contents, arguments=None):
        """Set correct command."""
        Container.__init__(self, contents, arguments)
        # TODO: only a single \with block is a valid argument - check this
        self.command = "\\book"


class BookPart(Container):

    """Book subdivision."""

    def __init__(self, contents, arguments=None):
        """Set correct command."""
        Container.__init__(self, contents, arguments)
        # TODO: only a single \with block is a valid argument - check this
        self.command = "\\bookpart"
