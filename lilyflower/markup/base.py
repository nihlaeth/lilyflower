"""Everything to do with markup blocks."""
from lilyflower.notecommands import NoteCommand
from lilyflower.container import Container
from lilyflower.errors import InvalidArgument


def validate_markup(data):
    """Check if object counts as markup."""
    if isinstance(data, MarkupContainer):
        pass
    elif isinstance(data, MarkupCommand):
        pass
    elif isinstance(data, MarkupText):
        pass
    else:
        raise InvalidArgument("Expected Markup item, not %r" % data)


class MarkupText(object):

    """Simple text for use inside markup blocks."""

    _inline = True

    def __init__(self, text):
        """Store text."""
        self._text = text
        # TODO: validation (what do we allow here?)


class MarkupCommand(NoteCommand):

    """Markup command."""


class MarkupContainer(Container, NoteCommand):

    """
    Stub for commands that are valid within markup blocks.

    Markup commands can be valid for a single expression, or
    followed by a block. They are either attached to a note,
    or stored in a variable that is then attached to a note.
    """

    _inline = True

    def __init__(self, content=None, arguments=None, position=""):
        """Store contents, arguments and optional position(^|-|_||)."""
        NoteCommand.__init__(self, position=position)
        Container.__init__(self, content, arguments)

    def _validate_content(self):
        """Make sure content belongs in a markup container."""
        for item in self._container:
            validate_markup(item)

    def __format__(self, format_spec):
        """Return lilypond code."""
        return "%s%s" % (
            self._position,
            Container.__format__(self, format_spec))


class Markup(MarkupContainer):

    """Markup block."""

    _command = "\\markup"
