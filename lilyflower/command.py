"""Non-container command."""
from lilyflower.errors import InvalidArgument


class Command(object):

    r"""
    Command stub.

    Every content-less command inherits from this. Not meant to be called
    directly.

    Use format() to get lilypond code.

    Usage::

        Command(*arguments)

    Parameters
    ==========
    *arguments:
        zero or more arguments. ``Command`` does not accept any, but
        subclasses can set their own requirements.

    Returns
    =======
    None

    Raises
    ======
    InvalidArgument:
        if there are too few, too many or the wrong type arguments.

    Notes
    =====

    See Also
    ========
    :class:`lilyflower.errors.InvalidArgument`

    Examples
    ========
    .. testsetup::

        from lilyflower.command import Command
        from lilyflower.errors import InvalidArgument

    .. doctest::

        >>> command = Command()
        >>> print format(command)
        \test
        >>> try:
        ...     Command("this is not a valid argument")
        ... except InvalidArgument as e:
        ...     print e
        Expects between 0 and 0 arguments.
    """

    _command = "\\test"
    _min_arguments = 0
    _max_arguments = 0
    _inline = False
    _validated_arguments = None

    def __init__(self, *arguments):
        """Store arguments."""
        if len(arguments) < self._min_arguments or \
                len(arguments) > self._max_arguments:
            raise InvalidArgument("Expects between %d and %d arguments." % (
                self._min_arguments, self._max_arguments))
        self._arguments = arguments
        self._validate_arguments()

    def _validate_arguments(self):
        """
        In-depth argument validation.

        Placeholder for children to overwrite.
        """
        pass

    def __format__(self, format_spec):
        """Return lilypond code."""
        indent_level = 0
        if format_spec != "":
            indent_level = int(format_spec)
        result = self._command
        if self._validated_arguments is not None:
            new_indent = indent_level + 1
            result += " " + " ".join(
                format(
                    item,
                    str(new_indent)) for item in self._validated_arguments)
        return result
