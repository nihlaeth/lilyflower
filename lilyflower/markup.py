"""Everything to do with markup blocks."""
# pylint: disable = relative-import,too-few-public-methods
import re
from notecommands import NoteCommand
from container import Container
from errors import InvalidArgument, InvalidContent


def _validate_ufloat(number):
    """Validate unsigned float."""
    regex = "^[0-9]+(\\.[0-9]*)?$"
    if re.match(regex, number) is None:
        raise InvalidArgument("Expected an unsigned float, not %r" % number)


def _validate_sfloat(number):
    """Validate signed float."""
    regex = "^-?[0-9]+(\\.[0-9]*)?$"
    if re.match(regex, number) is None:
        raise InvalidArgument("Expected a signed float, not %r" % number)


class MarkupText(object):

    """Simple text for use inside markup blocks."""

    inline = True

    def __init__(self, text):
        """Store text."""
        self.text = text
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

    inline = True

    def validate_content(self):
        """Make sure content belongs in a markup container."""
        for item in self.container:
            # the list of allowed content here is not complete yet
            # you can override settings in markup blocks for example
            # and use variables (I think)
            if isinstance(item, MarkupContainer):
                pass
            elif isinstance(item, MarkupCommand):
                pass
            elif isinstance(item, MarkupText):
                pass
            else:
                raise InvalidContent(
                    "%s does not belong in a markup container" % repr(item))


class Markup(MarkupContainer):

    """Markup block."""

    command = "\\markup"


class Bold(MarkupContainer):

    """Bold text."""

    command = "\\bold"


class Italic(MarkupContainer):

    """Italic text."""

    command = "\\italic"


class AbsFontSize(MarkupContainer):

    """Set absolute font size."""

    command = "\\abs-fontsize"
    min_arguments = 1
    max_arguments = 1

    def validate_arguments(self):
        """Make sure we get a scheme number (#N)."""
        _validate_ufloat(str(self.arguments[0]))
        self.validated_arguments.append("#" + str(self.arguments[0]))


class Box(MarkupContainer):

    """Draw a box around some text."""

    command = "\\box"


class Caps(MarkupContainer):

    """ALLCAPS."""

    command = "\\caps"


class DynamicFont(MarkupContainer):

    """Use the dynamic font (only contains f s z m p and r)."""

    command = "\\dynamic"


class FingerFont(MarkupContainer):

    """Use the finger font."""

    command = "\\finger"


class FontCaps(MarkupContainer):

    """Set font-shape to caps (font has to support this)."""

    command = "\\fontCaps"


class FontSize(MarkupContainer):

    """Set font-size."""

    command = "\\fontsize"
    min_arguments = 1
    max_arguments = 1

    def validate_arguments(self):
        """Make sure we get a scheme number(#-N)."""
        _validate_sfloat(str(self.arguments[0]))
        self.validated_arguments.append("#" + str(self.arguments[0]))


class Huge(MarkupContainer):

    """Set font-size to +2."""

    command = "\\huge"


class Large(MarkupContainer):

    """Set font-size to +1."""

    command = "\\large"


class Larger(MarkupContainer):

    """Increase font size relative to current setting."""

    command = "\\larger"


class Magnify(MarkupContainer):

    """Enlarge font (only works if font name is set)."""

    command = "\\magnify"
    min_arguments = 1
    max_arguments = 1

    def validate_arguments(self):
        """Make sure we get a scheme number(#N)."""
        _validate_ufloat(str(self.arguments[0]))
        self.validated_arguments.append("#" + str(self.arguments[0]))


class Medium(MarkupContainer):

    """Contrast to bold."""

    command = "\\medium"


class NormalSizeSub(MarkupContainer):

    """Set font size to normal subscript."""

    command = "\\normal-size-sub"


class NormalSizeSuper(MarkupContainer):

    """Set font size to normal superscript."""

    command = "\\normal-size-super"


class NormalText(MarkupContainer):

    """Set everything except size to default."""

    command = "\\normal-text"


class NumberFont(MarkupContainer):

    """Set number font family (only numbers and some punctuation)."""

    command = "\\number"


class Replace(MarkupContainer):

    """Replace a string by another."""

    command = "\\replace"
    min_arguments = 1
    max_arguments = 1

    # TODO: validate replacement list, maybe allow for a python list
    # and convert?


class RomanFont(MarkupContainer):

    """Set roman font family."""

    command = "\\roman"


class SansFont(MarkupContainer):

    """Set sans font family."""

    command = "\\sans"


class Simple(MarkupCommand):

    """Simple text."""

    command = "\\simple"
    min_arguments = 1
    max_arguments = 1

    def validate_arguments(self):
        """Make sure we received text."""
        self.validated_arguments[0] = "#\"%s\"" % str(self.args[0])


class Small(MarkupContainer):

    """Set font-size to -1."""

    command = "\\small"


class SmallCaps(MarkupContainer):

    """Small font-size, all-caps."""

    command = "\\smallCaps"


class Smaller(MarkupContainer):

    """Decrease font-size relative to current setting."""

    command = "\\smaller"


class Sub(MarkupContainer):

    """Subscript."""

    command = "\\sub"


class Super(MarkupContainer):

    """Superscript."""

    command = "\\super"


class Teeny(MarkupContainer):

    """Set font size to -3."""

    command = "\\teeny"


class TextFont(MarkupContainer):

    """Set font to text family."""

    command = "\\text"


class Tiny(MarkupContainer):

    """Set font size to -2."""

    command = "\\tiny"


class TypeWriterFont(MarkupContainer):

    """Set font family to typewriter."""

    command = "\\typewriter"


class Underline(MarkupContainer):

    """Underline text."""

    command = "\\underline"


class Upright(MarkupContainer):

    """Upright in contrast to italic."""

    command = "\\upright"
