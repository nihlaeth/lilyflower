"""Container derived classes."""
import datetime

from container import Container


class LilyFile(Container):

    """Container for a single lilypond file."""

    _delimiter_pre = ""
    _delimiter_post = ""

    def __format__(self, _):
        """Return lilypond code."""
        # root container does not indent its children
        result = "%% Created with lilyflower at %s\n" % datetime.datetime.now()
        inline_previous = False
        for item in self._container:
            separator = "\n"
            inline_current = item._inline
            # the only time we need a space as separator is when
            # both the current and previous item are inline
            if inline_previous and inline_current:
                separator = " "
            result += "%s%s" % (separator, format(item))
            inline_previous = inline_current
        return result


class Book(Container):

    """Book container."""

    _command = "\\book"


class BookPart(Container):

    """Book subdivision."""

    _command = "\\bookpart"


class With(Container):

    """With block."""

    _command = "\\with"


class Score(Container):

    """Score block."""

    _command = "\\score"


class Staff(Container):

    """Staff block."""

    _command = "\\staff"


class Header(Container):

    """Header block."""

    _command = "\\header"


class Layout(Container):

    """Layout block."""

    _command = "\\layout"


class Midi(Container):

    """Midi block."""

    _command = "\\midi"


class Parallel(Container):

    """Parallel block."""

    delimiter_pre = "<<"
    delimiter_post = ">>"


class Voice(Container):

    """Voice block."""

    _command = "\\voice"


class Paper(Container):

    """Paper block."""

    _command = "\\paper"


class New(Container):

    """New block."""

    _command = "\\new"
    _min_arguments = 1
    _max_arguments = 1

    # TODO: we need argument validation here!


class Lyrics(Container):

    """Lyrics block."""

    _command = "\\lyrics"


class AddLyrics(Container):

    """AddLyrics block."""

    _command = "\\addlyrics"


class LyricsTo(Container):

    """LyricsTo block."""

    _command = "\\lyricsto"


class Absolute(Container):

    """Absolute block."""

    _command = "\\absolute"


class Relative(Container):

    """Relative block."""

    _command = "\\relative"
    _max_arguments = 1

    # TODO: we need argument validation here!


class Transpose(Container):

    """Transpose block."""

    _command = "\\transpose"
    _min_arguments = 2
    _max_arguments = 2

    # TODO: we need argument validation here!


class Markup(Container):

    """Markup block."""

    _command = "\\markup"


class Repeat(Container):

    """Repeat block."""

    _command = "\\repeat"
    _min_arguments = 2
    _max_arguments = 2

    # TODO: we need argument validation here!


class Measure(Container):

    """
    Contains one measure.

    This does not have knowledge of note duration, or time signature.
    It's simply a collection of music that ends with a bar check
    and a newline. Useful for organization, and error checking,
    but not much else.
    """

    _max_arguments = 1
    _delimiter_pre = ""
    _delimiter_post = ""

    # TODO: argument validation! make sure we got 0 or 1 bar objects.

    def __format__(self, format_spec):
        """Return lilypond code."""
        indent_level = 0
        if format_spec is not "":
            indent_level = int(format_spec)
        result = " ".join([
            format(item, str(indent_level + 1)) for item in self._container])
        if len(self._arguments) < 1:
            result += " |"
        else:
            result += " %s" % format(self._arguments[0])
        return result
