"""Everything to do with markup blocks."""
from lilyflower.errors import InvalidArgument
from lilyflower.schemedata import (
    UnsignedFloat,
    SignedFloat,
    String,
    SignedInt,
    Pair)
from lilyflower.markup.base import (
    MarkupContainer, MarkupCommand, validate_markup)


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
        validate_markup(self._arguments[0])
        validate_markup(self._arguments[1])
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
        validate_markup(self._arguments[2])

        # markup_left (should be markup element)
        validate_markup(self._arguments[3])

        # markup_right (should be markup element)
        validate_markup(self._arguments[4])

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


class PutAdjacent(MarkupCommand):

    r"""
    Put `arg2` next to `arg1` without moving `arg1`.

    Usage::
        PutAdjacent(axis, direction, arg1, arg2, position="")

    Parameters
    ==========
    axis: Axis, SignedInt
        along which axis to move
    direction: Direction, SignedFloat
        in which direction to move
    arg1: markup
        markup to which arg2 should be put adjacent
    arg2: markup
        markup to put adjacent to arg1
    position: str (^|-|_|), optional, named, default=""
        position relative to note

    Returns
    =======
    None

    Raises
    ======
    InvalidArgument:
        if any of the arguments don't have the correct type, or
        if the wrong number of arguments is supplied.

    Notes
    =====
    Technically this should be a container with two separate contents
    for `arg1` and `arg2`. This would complicate things programmatically
    though, so we decided against it. If you need `arg1` or `arg2` to be
    more than one element, wrap them in a
    :class:`lilyflower.markup.base.MarkupContainer`.

    See Also
    ========
    :class:`lilyflower.command.Command`
    :class:`lilyflower.markup.base.MarkupCommand`
    :class:`lilyflower.errors.InvalidArgument`
    :class:`lilyflower.schemedata.SignedInt`
    :class:`lilyflower.schemedata.SignedFloat`
    :class:`lilyflower.schemedata.Axis`
    :class:`lilyflower.schemedata.Direction`
    :func:`lilyflower.markup.base.validate_markup`

    References
    ==========
    `Lilypond \\put-adjacent documentation
    <http://lilypond.org/doc/v2.18/Documentation/notation/align#index-_005cput_002dadjacent-1>`_

    Examples
    ========
    .. testsetup::

        from lilyflower.markup.font import Bold
        from lilyflower.markup.align import PutAdjacent
        from lilyflower.errors import InvalidArgument
        from lilyflower.schemedata import Axis, Direction

    .. doctest::

        >>> c = PutAdjacent(Axis('x'), Direction('up'), Bold([]), Bold([]))
        >>> print format(c)
        \put-adjacent #X #UP \bold {
          } \bold {
          }
        >>> try:
        ...     PutAdjacent(Direction('up'), Axis('y'), Bold([]), Bold([]))
        ... except InvalidArgument as e:
        ...     print e
        Expected an Axis(SchemeData) or SignedInt(SchemeData) as the first ...
    """

    _command = "\\put-adjacent"
    _min_arguments = 4
    _max_arguments = 4

    def _validate_arguments(self):
        if not isinstance(self._arguments[0], SignedInt):
            raise InvalidArgument(
                "Expected an Axis(SchemeData) or SignedInt(SchemeData) "
                "as the first argument, not %r" % self._arguments[0])
        if not isinstance(self._arguments[1], SignedFloat):
            raise InvalidArgument(
                "Expected a Direction(SchemeData) or SignedFloat(SchemeDat)"
                " object as the second argument, not %r" % self._arguments[1])
        validate_markup(self._arguments[2])
        validate_markup(self._arguments[3])
        self._validated_arguments = []
        self._validated_arguments.extend(self._arguments)


class Raise(MarkupContainer):

    r"""
    Raise `content` horizontally by `amount`.

    Usage::
        Raise(content, [amount], position="")

    Parameters
    ==========
    content: list, markup, optional
        contents of raise block
    amount: SignedFloat
        how much to raise content
    position: string (^|-|_|), optional, default=""
        position relative to the note this is attached to

    Returns
    =======
    None

    Raises
    ======
    InvalidContent: UNIMPLEMENTED
        if any content items are not considered markup
    InvalidArgument:
        if any of the arguments don't have the correct type, or
        if the wrong number of arguments is supplied.

    Notes
    =====

    See Also
    ========
    :class:`lilyflower.container.Container`
    :class:`lilyflower.markup.base.MarkupContainer`
    :class:`lilyflower.errors.InvalidArgument`
    :class:`lilyflower.schemedata.SignedFloat`

    References
    ==========
    `Lilypond \\raise documentation
    <http://lilypond.org/doc/v2.18/Documentation/notation/align#index-_005craise-3>`_

    Examples
    ========
    .. testsetup::

        from lilyflower.markup.align import Raise
        from lilyflower.errors import InvalidArgument
        from lilyflower.schemedata import SignedFloat

    .. doctest::

        >>> c = Raise([], [SignedFloat(5)])
        >>> print format(c)
        \raise #5 {
        }
        >>> try:
        ...     Raise(arguments=[5])
        ... except InvalidArgument as e:
        ...     print e
        Expected a SignedFloat(SchemeData) as first argument, not 5
    """

    _command = "\\raise"
    _min_arguments = 1
    _max_arguments = 1

    def _validate_arguments(self):
        if not isinstance(self._arguments[0], SignedFloat):
            raise InvalidArgument(
                "Expected a SignedFloat(SchemeData) as first argument,"
                " not %r" % self._arguments[0])
        else:
            self._validated_arguments = [self._arguments[0]]
