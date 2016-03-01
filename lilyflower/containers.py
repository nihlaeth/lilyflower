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

    command = "\\lyricto"


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
