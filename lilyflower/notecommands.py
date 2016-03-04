"""Commands that attach to a tone."""
from command import Command
from errors import InvalidArgument
import re


class NoteCommand(Command):

    """Commands that attach to a tone."""

    _inline = True

    def __init__(self, *arguments, **kwargs):
        """Set arguments and position(^|-|_|).

        Syntax: __init__(*arguments, position=(^|-|_|))
        """
        Command.__init__(self, *arguments)
        if 'position' not in kwargs:
            self._position = ""
        else:
            self._position = kwargs['position']
        if re.match("^[\\^\\-_]?$", self._position) is None:
            raise InvalidArgument(
                "Expected (^|-|_|) as position, not %r" % self._position)

    def __format__(self, format_spec):
        """Return lilypond code."""
        return "%s%s" % (self._position, Command.__format__(self, format_spec))
