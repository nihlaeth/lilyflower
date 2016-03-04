"""Everything to do with markup blocks."""
# pylint: disable = relative-import,too-few-public-methods
from notecommands import NoteCommand
from container import Container
from errors import InvalidArgument
from schemedata import (
    UnsignedFloat,
    SignedFloat,
    AssociationList,
    String,
    SignedInt)


def _validate_markup(data):
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

    def __init__(self, content=None, arguments=None, position=""):
        """Store contents, arguments and optional position(^|-|_||)."""
        NoteCommand.__init__(self, position=position)
        Container.__init__(self, content, arguments)

    def validate_content(self):
        """Make sure content belongs in a markup container."""
        for item in self.container:
            _validate_markup(item)

    def __format__(self, format_spec):
        """Return lilypond code."""
        return "%s%s" % (
            self.position,
            Container.__format__(self, format_spec))


class Markup(MarkupContainer):

    """Markup block."""

    command = "\\markup"


#
# Font related stuff
#


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
        """Make sure we get a scheme number (UnsignedFloat)."""
        if not isinstance(self.arguments[0], UnsignedFloat):
            raise InvalidArgument(
                "Expected UnsignedFloat(SchemeData),"
                " not %r" % self.arguments[0])
        self.validated_arguments.append(self.arguments[0])


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
        """Make sure we get a scheme number(SignedFloat)."""
        if not isinstance(self.arguments[0], SignedFloat):
            raise InvalidArgument(
                "Expected SignedFloat(SchemeData), not %r" % self.arguments[0])
        self.validated_arguments.append(self.arguments[0])


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
        """Make sure we get a SchemeData String."""
        if not isinstance(self.arguments[0], String):
            raise InvalidArgument(
                "Expected String(SchemeData), not %r" % self.arguments[0])
        self.validated_arguments.append(self.arguments[0])


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

    def validate_arguments(self):
        """Make sure we got passed an AssociationList(SchemeData)."""
        if not isinstance(self.arguments[0], AssociationList):
            raise InvalidArgument(
                "Expected an AssociationList(SchemeData),"
                " not %r" % self.arguments[0])
        self.validated_arguments.append(self.arguments[0])


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
        """Make sure we received a SchemeData String."""
        if not isinstance(self.args[0], String):
            raise InvalidArgument(
                "Expected a String(SchemeData), not %r" % self.args[0])
        self.validated_arguments[0] = self.args[0]


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


#
# Alignment related stuff
#


class CenterAlign(MarkupCommand):

    """Align to its X center (whatever that means)."""

    command = "\\center-align"
    min_arguments = 1
    max_arguments = 1

    def validate_arguments(self):
        """Make sure argument is a markup expression."""
        _validate_markup(self.args[0])
        self.validated_arguments.append(self.args[0])


class CenterColumn(MarkupContainer):

    """Align in a centered column."""

    command = "\\center-column"


class Column(MarkupContainer):

    """Stack contents vertically."""

    command = "\\column"


class Combine(MarkupCommand):

    """Print two markups on top of each other."""

    command = "\\combine"
    min_arguments = 2
    max_arguments = 2

    def validate_arguments(self):
        """Make sure arguments count as markup."""
        _validate_markup(self.args[0])
        _validate_markup(self.args[1])
        self.validated_arguments.append(self.args[0])
        self.validated_arguments.append(self.args[1])


class Concat(MarkupContainer):

    """Combine contents in a horizontal line without space in between."""

    command = "\\concat"


class DirColumn(MarkupContainer):

    """Put contents in column, according to the direction layout property."""

    command = "\\dir-column"


class FillLine(MarkupContainer):

    """Space contents over entire width of line-width layout property."""

    command = "\\fill-line"


class FillWithPattern(MarkupCommand):

    """
    Fill horizontal line with two markup elements and a pattern.

    Usage:
    FillWithPattern(space, direction, pattern, markup_left, markup_right)
    Arguments:
    space -> UnsignedFloat(SchemeData) - space in between patterns
    direction -> Direction(SchemeData) - aligned to the direction markup
    pattern -> Markup element - pattern to fill line with
    markup_left -> Markup element - to be displayed at the left of pattern
    markup_right -> Markup element - to be displayed at the right of pattern
    """

    command = "\\fill-with-pattern"
    min_arguments = 5
    max_arguments = 5

    def validate_arguments(self):
        """Make sure it at least appears valid."""
        # space (should be Int)
        if not isinstance(self.args[0], UnsignedFloat):
            raise InvalidArgument(
                "Expected UnsignedFloat(SchemeData), not %r", self.args[0])
        # direction (should be Direction)
        if not isinstance(self.args[1], SignedFloat):
            raise InvalidArgument(
                "Expected Direction(SchemeData), "
                " or a SignedFloat(SchemeData), not %r", self.args[1])

        # pattern (should be markup element)
        _validate_markup(self.args[2])

        # markup_left (should be markup element)
        _validate_markup(self.args[3])

        # markup_right (should be markup element)
        _validate_markup(self.args[4])

        self.validated_arguments.extend(self.args)


class GeneralAlign(MarkupContainer):

    """Align content in <axis> direction to the <dir> side."""

    command = "\\general-align"
    min_arguments = 2
    max_arguments = 2

    def validate_arguments(self):
        """Make sure arguments make some kind of sense."""
        # axis (should be int or axis)
        if not isinstance(self.arguments[0], SignedInt):
            raise InvalidArgument(
                "Expected SignedInt(SchemeData) or "
                "Axis(SchemeData), not %r" % self.arguments[0])
        # direction
        if not isinstance(self.arguments[1], SignedFloat):
            raise InvalidArgument(
                "Expected Direction(SchemeData), "
                " or a SignedFloat(SchemeData), not %r", self.arguments[1])
        self.validated_arguments.append(self.arguments[0])
        self.validated_arguments.append(self.arguments[1])
