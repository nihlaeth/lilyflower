"""Container derived classes."""
import datetime

from container import Container


class LilyFile(Container):

    """Container for a single lilypond file."""

    delimiter_pre = ""
    delimiter_post = ""

    def __format__(self, _):
        """Return lilypond code."""
        # root container does not indent its children
        result = "%% Created with lilyflower at %s\n" % datetime.datetime.now()
        inline_previous = False
        for item in self.container:
            separator = "\n"
            inline_current = item.inline
            # the only time we need a space as separator is when
            # both the current and previous item are inline
            if inline_previous and inline_current:
                separator = " "
            result += "%s%s" % (separator, format(item))
            inline_previous = inline_current
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


class Staff(Container):

    """Staff block."""

    command = "\\staff"


class Header(Container):

    """Header block."""

    command = "\\header"


class Layout(Container):

    """Layout block."""

    command = "\\layout"


class Midi(Container):

    """Midi block."""

    command = "\\midi"


class Parallel(Container):

    """Parallel block."""

    delimiter_pre = "<<"
    delimiter_post = ">>"


class Voice(Container):

    """Voice block."""

    command = "\\voice"


class Paper(Container):

    """Paper block."""

    command = "\\paper"


class New(Container):

    """New block."""

    command = "\\new"
    min_arguments = 1
    max_arguments = 1

    # TODO: we need argument validation here!


class Lyrics(Container):

    """Lyrics block."""

    command = "\\lyrics"


class AddLyrics(Container):

    """AddLyrics block."""

    command = "\\addlyrics"


class LyricsTo(Container):

    """LyricsTo block."""

    command = "\\lyricsto"


class Absolute(Container):

    """Absolute block."""

    command = "\\absolute"


class Relative(Container):

    """Relative block."""

    command = "\\relative"
    max_arguments = 1

    # TODO: we need argument validation here!


class Transpose(Container):

    """Transpose block."""

    command = "\\transpose"
    min_arguments = 2
    max_arguments = 2

    # TODO: we need argument validation here!


class Markup(Container):

    """Markup block."""

    command = "\\markup"


class Repeat(Container):

    """Repeat block."""

    command = "\\repeat"
    min_arguments = 2
    max_arguments = 2

    # TODO: we need argument validation here!


class Measure(Container):

    """
    Contains one measure.

    This does not have knowledge of note duration, or time signature.
    It's simply a collection of music that ends with a bar check
    and a newline. Useful for organization, and error checking,
    but not much else.
    """

    max_arguments = 1
    delimiter_pre = ""
    delimiter_post = ""

    # TODO: argument validation! make sure we got 0 or 1 bar objects.

    def __format__(self, format_spec):
        """Return lilypond code."""
        indent_level = 0
        if format_spec is not "":
            indent_level = int(format_spec)
        result = "  " * indent_level
        result += " ".join([
            format(item, str(indent_level + 1)) for item in self.container])
        if len(self.arguments) < 1:
            result += " |"
        else:
            result += " %s" % format(self.arguments[0])
        return result
