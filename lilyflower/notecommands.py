"""Commands that attach to a tone."""
from command import Command
from errors import InvalidArgument
import re


class NoteCommand(Command):

    """Commands that attach to a tone."""

    inline = True

    def __init__(self, *arguments, **kwargs):
        """Set arguments and position(^|-|_|).

        Syntax: __init__(*arguments, position=(^|-|_|))
        """
        Command.__init__(self, *arguments)
        if 'position' not in kwargs:
            self.position = ""
        else:
            self.position = kwargs['position']
        if re.match("^[\\^\\-_]?$", self.position) is None:
            raise InvalidArgument(
                "Expected (^|-|_|) as position, not %r" % self.position)

    def __format__(self, format_spec):
        """Return lilypond code."""
        return "%s%s" % (self.position, Command.__format__(self, format_spec))
