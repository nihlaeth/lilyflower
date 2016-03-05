"""Non-container commands."""
from lilyflower.command import Command
from lilyflower.errors import InvalidArgument


class Bar(Command):

    r"""
    Bar checks and delimiters.

    Usage::

        Bar(bar_string)

    Parameters
    ==========
    bar_string: str (default="|")
        valid lilypond bar type. Custom bar types are not supported at
        this time.

    Returns
    =======
    None

    Raises
    ======
    InvalidArgument:
        when more or less than one argument is provided, and when the
        argument is not a valid bar type.

    Notes
    =====

    See Also
    ========
    :class:`lilyflower.command.Command`
    :class:`lilyflower.errors.InvalidArgument`

    References
    ==========
    `Lilypond \\bar documentation
    <http://lilypond.org/doc/v2.18/Documentation/notation/bars#index-_005cbar-1>`_

    Examples
    ========
    .. testsetup::

        from lilyflower.commands import Bar
        from lilyflower.errors import InvalidArgument

    .. doctest::

        >>> print format(Bar())
        \bar "|"
        >>> print format(Bar("|."))
        \bar "|."
        >>> try:
        ...     Bar("invalid bar")
        ... except InvalidArgument as e:
        ...     print e
        'invalid bar' not a valid bar type.
    """

    _command = "\\bar"
    _min_arguments = 0
    _max_arguments = 1
    _inline = True

    def _validate_arguments(self):
        """Make sure argument is a valid bar."""
        valid_bars = [
            ".",
            "|",
            "||",
            ".|",
            "|.",
            "..",
            "|.|",
            ";",
            "!",
            ".|:",
            ":..:",
            ":|.|:",
            ":|.:",
            ":.|.:",
            "[|:",
            ":|][|:",
            ":|]",
            ":|.",
            "'",
            "k",
            "S",
            "S-|",
            "S-S",
            ".|:-||",
            ":|.S",
            ":|.S",
            ":|.S-S",
            ":|.S-S",
            "S.|:-S",
            "S.|:-S",
            "S.|:",
            "S.|:",
            ":|.S.|:",
            ":|.S.|:",
            ":|.S.|:-S",
            ":|.S.|:-S"]
        # TODO: add support for custom bar definitions
        if len(self._arguments) == 0:
            self._validated_arguments = ["\"|\""]
        elif self._arguments[0] not in valid_bars:
            raise InvalidArgument(
                "%r not a valid bar type." % self._arguments[0])
        else:
            self._validated_arguments = ["\"%s\"" % self._arguments[0]]
