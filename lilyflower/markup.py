"""Everything to do with markup blocks."""
# pylint: disable = too-few-public-methods
from lilyflower.notecommands import NoteCommand
from lilyflower.container import Container
from lilyflower.errors import InvalidArgument
from lilyflower.schemedata import (
    UnsignedFloat,
    SignedFloat,
    AssociationList,
    String,
    SignedInt,
    Pair)


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
            _validate_markup(item)

    def __format__(self, format_spec):
        """Return lilypond code."""
        return "%s%s" % (
            self._position,
            Container.__format__(self, format_spec))


class Markup(MarkupContainer):

    """Markup block."""

    _command = "\\markup"


#
# Font related stuff
#


class Bold(MarkupContainer):

    """Bold text."""

    _command = "\\bold"


class Italic(MarkupContainer):

    """Italic text."""

    _command = "\\italic"


class AbsFontSize(MarkupContainer):

    """Set absolute font size."""

    _command = "\\abs-fontsize"
    _min_arguments = 1
    _max_arguments = 1

    def _validate_arguments(self):
        """Make sure we get a scheme number (UnsignedFloat)."""
        if not isinstance(self._arguments[0], UnsignedFloat):
            raise InvalidArgument(
                "Expected UnsignedFloat(SchemeData),"
                " not %r" % self._arguments[0])
        self._validated_arguments.append(self._arguments[0])


class Box(MarkupContainer):

    """Draw a box around some text."""

    _command = "\\box"


class Caps(MarkupContainer):

    """ALLCAPS."""

    _command = "\\caps"


class DynamicFont(MarkupContainer):

    """Use the dynamic font (only contains f s z m p and r)."""

    _command = "\\dynamic"


class FingerFont(MarkupContainer):

    """Use the finger font."""

    _command = "\\finger"


class FontCaps(MarkupContainer):

    """Set font-shape to caps (font has to support this)."""

    _command = "\\fontCaps"


class FontSize(MarkupContainer):

    """Set font-size."""

    _command = "\\fontsize"
    _min_arguments = 1
    _max_arguments = 1

    def _validate_arguments(self):
        """Make sure we get a scheme number(SignedFloat)."""
        if not isinstance(self._arguments[0], SignedFloat):
            raise InvalidArgument(
                "Expected SignedFloat(SchemeData), "
                "not %r" % self._arguments[0])
        self._validated_arguments.append(self._arguments[0])


class Huge(MarkupContainer):

    """Set font-size to +2."""

    _command = "\\huge"


class Large(MarkupContainer):

    """Set font-size to +1."""

    _command = "\\large"


class Larger(MarkupContainer):

    """Increase font size relative to current setting."""

    _command = "\\larger"


class Magnify(MarkupContainer):

    """Enlarge font (only works if font name is set)."""

    _command = "\\magnify"
    _min_arguments = 1
    _max_arguments = 1

    def _validate_arguments(self):
        """Make sure we get a SchemeData String."""
        if not isinstance(self._arguments[0], String):
            raise InvalidArgument(
                "Expected String(SchemeData), not %r" % self._arguments[0])
        self._validated_arguments.append(self._arguments[0])


class Medium(MarkupContainer):

    """Contrast to bold."""

    _command = "\\medium"


class NormalSizeSub(MarkupContainer):

    """Set font size to normal subscript."""

    _command = "\\normal-size-sub"


class NormalSizeSuper(MarkupContainer):

    """Set font size to normal superscript."""

    _command = "\\normal-size-super"


class NormalText(MarkupContainer):

    """Set everything except size to default."""

    _command = "\\normal-text"


class NumberFont(MarkupContainer):

    """Set number font family (only numbers and some punctuation)."""

    _command = "\\number"


class Replace(MarkupContainer):

    """Replace a string by another."""

    _command = "\\replace"
    _min_arguments = 1
    _max_arguments = 1

    def _validate_arguments(self):
        """Make sure we got passed an AssociationList(SchemeData)."""
        if not isinstance(self._arguments[0], AssociationList):
            raise InvalidArgument(
                "Expected an AssociationList(SchemeData),"
                " not %r" % self._arguments[0])
        self._validated_arguments.append(self._arguments[0])


class RomanFont(MarkupContainer):

    """Set roman font family."""

    _command = "\\roman"


class SansFont(MarkupContainer):

    """Set sans font family."""

    _command = "\\sans"


class Simple(MarkupCommand):

    """Simple text."""

    _command = "\\simple"
    _min_arguments = 1
    _max_arguments = 1

    def _validate_arguments(self):
        """Make sure we received a SchemeData String."""
        if not isinstance(self._arguments[0], String):
            raise InvalidArgument(
                "Expected a String(SchemeData), not %r" % self._arguments[0])
        self._validated_arguments[0] = self._arguments[0]


class Small(MarkupContainer):

    """Set font-size to -1."""

    _command = "\\small"


class SmallCaps(MarkupContainer):

    """Small font-size, all-caps."""

    _command = "\\smallCaps"


class Smaller(MarkupContainer):

    """Decrease font-size relative to current setting."""

    _command = "\\smaller"


class Sub(MarkupContainer):

    """Subscript."""

    _command = "\\sub"


class Super(MarkupContainer):

    """Superscript."""

    _command = "\\super"


class Teeny(MarkupContainer):

    """Set font size to -3."""

    _command = "\\teeny"


class TextFont(MarkupContainer):

    """Set font to text family."""

    _command = "\\text"


class Tiny(MarkupContainer):

    """Set font size to -2."""

    _command = "\\tiny"


class TypeWriterFont(MarkupContainer):

    """Set font family to typewriter."""

    _command = "\\typewriter"


class Underline(MarkupContainer):

    """Underline text."""

    _command = "\\underline"


class Upright(MarkupContainer):

    """Upright in contrast to italic."""

    _command = "\\upright"


#
# Alignment related stuff
#


class CenterAlign(MarkupContainer):

    """Align to its X center (whatever that means)."""

    _command = "\\center-align"


class CenterColumn(MarkupContainer):

    """Align in a centered column."""

    _command = "\\center-column"


class Column(MarkupContainer):

    """Stack contents vertically."""

    _command = "\\column"


class Combine(MarkupCommand):

    """Print two markups on top of each other."""

    _command = "\\combine"
    _min_arguments = 2
    _max_arguments = 2

    def _validate_arguments(self):
        """Make sure arguments count as markup."""
        _validate_markup(self._arguments[0])
        _validate_markup(self._arguments[1])
        self._validated_arguments.append(self._arguments[0])
        self._validated_arguments.append(self._arguments[1])


class Concat(MarkupContainer):

    """Combine contents in a horizontal line without space in between."""

    _command = "\\concat"


class DirColumn(MarkupContainer):

    """Put contents in column, according to the direction layout property."""

    _command = "\\dir-column"


class FillLine(MarkupContainer):

    """Space contents over entire width of line-width layout property."""

    _command = "\\fill-line"


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

    _command = "\\fill-with-pattern"
    _min_arguments = 5
    _max_arguments = 5

    def _validate_arguments(self):
        """Make sure it at least appears valid."""
        # space (should be Int)
        if not isinstance(self._arguments[0], UnsignedFloat):
            raise InvalidArgument(
                "Expected UnsignedFloat(SchemeData), "
                "not %r", self._arguments[0])
        # direction (should be Direction)
        if not isinstance(self._arguments[1], SignedFloat):
            raise InvalidArgument(
                "Expected Direction(SchemeData), "
                " or a SignedFloat(SchemeData), not %r", self._arguments[1])

        # pattern (should be markup element)
        _validate_markup(self._arguments[2])

        # markup_left (should be markup element)
        _validate_markup(self._arguments[3])

        # markup_right (should be markup element)
        _validate_markup(self._arguments[4])

        self._validated_arguments.extend(self._arguments)


class GeneralAlign(MarkupContainer):

    """Align content in <axis> direction to the <dir> side."""

    _command = "\\general-align"
    _min_arguments = 2
    _max_arguments = 2

    def _validate_arguments(self):
        """Make sure arguments make some kind of sense."""
        # axis (should be int or axis)
        if not isinstance(self._arguments[0], SignedInt):
            raise InvalidArgument(
                "Expected SignedInt(SchemeData) or "
                "Axis(SchemeData), not %r" % self._arguments[0])
        # direction
        if not isinstance(self._arguments[1], SignedFloat):
            raise InvalidArgument(
                "Expected Direction(SchemeData), "
                " or a SignedFloat(SchemeData), not %r", self._arguments[1])
        self._validated_arguments.append(self._arguments[0])
        self._validated_arguments.append(self._arguments[1])


class HAlign(MarkupContainer):

    """Horizontal align."""

    _command = "\\halign"
    _min_arguments = 1
    _max_arguments = 1

    def _validate_arguments(self):
        """Validate arguments."""
        # direction
        if not isinstance(self._arguments[0], SignedFloat):
            raise InvalidArgument(
                "Expected Direction(SchemeData), "
                " or a SignedFloat(SchemeData), not %r", self._arguments[0])
        self._validated_arguments.append(self._arguments[0])


class HCenterIn(MarkupContainer):

    """Center horiz. within a box of extending len/2 to both sides."""

    _command = "\\halign-in"
    _min_arguments = 1
    _max_arguments = 1

    def _validate_arguments(self):
        """Validate arguments."""
        if not isinstance(self._arguments[0], SignedFloat):
            raise InvalidArgument(
                "Expected SignedFloat(SchemeData), "
                "not %r" % self._arguments[0])
        self._validated_arguments.append(self._arguments[0])


class HSpace(MarkupCommand):

    """Create invisible object taking up horizontal space."""

    _command = "\\hspace"
    _min_arguments = 1
    _max_arguments = 1

    def _validate_arguments(self):
        """Validate arguments."""
        if not isinstance(self._arguments[0], SignedFloat):
            raise InvalidArgument(
                "Expected SignedFloat(SchemeData), "
                "not %r" % self._arguments[0])
        self._validated_arguments.append(self._arguments[0])


class JustifyField(MarkupCommand):

    """Justify markup in field."""

    _command = "\\justify-field"
    _min_arguments = 1
    _max_arguments = 1

    # TODO: validate argument (scheme field)


class Justify(MarkupContainer):

    """Justify contents."""

    _command = "\\justify"


class JustifyString(MarkupCommand):

    """Justify a string."""

    _command = "\\jusify-string"
    _min_arguments = 1
    _max_arguments = 1

    def _validate_arguments(self):
        """Validate arguments."""
        if not isinstance(self._arguments[0], String):
            raise InvalidArgument(
                "Expected String(SchemeData), not %r" % self._arguments[0])
        self._validated_arguments.append(self._arguments[0])


class LeftAlign(MarkupContainer):

    """Align contents to the left."""

    _command = "\\left-align"


class LeftColumn(MarkupContainer):

    """Align contents to the left in a column."""

    _command = "\\left-column"


class Line(MarkupContainer):

    """Put contents in horizontal line."""

    _command = "\\line"


class Lower(MarkupContainer):

    """Lower contents vertically."""

    _command = "\\lower"
    _min_arguments = 1
    _max_arguments = 1

    def _validate_arguments(self):
        """Validate arguments."""
        if not isinstance(self._arguments[0], SignedFloat):
            raise InvalidArgument(
                "Expected SignedFloat(SchemeData), "
                "not %r" % self._arguments[0])
        self._validated_arguments.append(self._arguments[0])


class PadAround(MarkupContainer):

    """Pad around contents."""

    _command = "\\pad-around"
    _min_arguments = 1
    _max_arguments = 1

    def _validate_arguments(self):
        """Validate arguments."""
        if not isinstance(self._arguments[0], SignedFloat):
            raise InvalidArgument(
                "Expected SignedFloat(SchemeData), "
                "not %r" % self._arguments[0])
        self._validated_arguments.append(self._arguments[0])


class PadMarkup(PadAround):

    """Same as PadAround."""

    _command = "\\pad-markup"


class PadToBox(MarkupContainer):

    """Make content take at least (-x . x) by (-y . y) space."""

    _command = "\\pad-to-box"
    _min_arguments = 2
    _max_arguments = 2

    def _validate_arguments(self):
        """Validate arguments."""
        for arg in self._arguments:
            if not isinstance(arg, Pair):
                raise InvalidArgument(
                    "Expected Pair(SchemeData), not %r" % arg)
            self._validated_arguments.append(arg)


class PadX(MarkupContainer):

    """Pad in the x direction."""

    _command = "\\pad-x"
    _min_arguments = 1
    _max_arguments = 1

    def _validate_arguments(self):
        """Validate arguments."""
        if not isinstance(self._arguments[0], SignedFloat):
            raise InvalidArgument(
                "Expected SignedFloat(SchemeData), "
                "not %r" % self._arguments[0])
        self._validated_arguments.append(self._arguments[0])
