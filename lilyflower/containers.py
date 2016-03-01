"""Container derived classes."""
import datetime

from container import Container


class LilyFile(Container):

    """Container for a single lilypond file."""

    delimiter_pre = ""
    delimiter_post = ""

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

    command = "\\book"


class BookPart(Container):

    """Book subdivision."""

    command = "\\bookpart"


class With(Container):

    """With block."""

    command = "\\with"


class Score(Container):

    """Score block."""

    command = "\\score"
