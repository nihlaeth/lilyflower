"""Everything to do with markup blocks."""
from lilyflower.errors import InvalidArgument
from lilyflower.schemedata import (
    UnsignedFloat,
    SignedFloat,
    AssociationList,
    String)
from lilyflower.markup.base import MarkupContainer, MarkupCommand


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
