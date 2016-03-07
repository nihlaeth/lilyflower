"""Basic building block for the object tree."""
from collections import OrderedDict
from lilyflower.errors import InvalidArgument


class Node(object):

    r"""
    Basic building block for the object tree.

    Usage:
        None - this class is meant to be inherited.

    Parameters
    ==========

    Raises
    ======

    Returns
    =======

    Notes
    =====

    See Also
    ========

    References
    ==========

    Examples
    ========

    """

    _tag = ""
    _types = ()
    _arguments = ()
    _stored_arguments = None
    _allowed_content = ()
    _inline = False
    _delimiter_open = "{"
    _delimiter_close = "}"
    _position = ""

    def __init__(self, *args, **kwargs):
        r"""
        Fancy parameter resolution.

        We get a bunch of arguments, and with the help of
        `self._arguments`, `self._types` and `self._allowed_content`,
        we have to determine what is what.

        We start with `kwargs`, because that's easiest. Anything that is
        not named `position` (for objects with 'attachment' type, or
        `content` (for objects where allowed_content is not None), should
        be in `self._arguments`.

        After that, we get started on `args`. We check if there
        is a `list` in `args` - this is the content. The rest is
        positional, with `self._arguments` first, and optionally a
        last `position` argument if object has `attachment` type.

        Then, if anything is missing that is not optional, or if we
        have a spare argument we can't place, we throw an
        `InvalidArgument` error.

        Then we do some content and argument validation, and store everything.
        """
        # Data prep
        self._stored_arguments = OrderedDict()
        args = list(args)

        # List what we expect
        arg_order = []
        arg_value = OrderedDict()
        for arg in self._arguments:
            arg_order.append(arg.name)
            arg_value[arg.name] = None
        if 'attachment' in self._types:
            arg_order.append('position')
            arg_value['position'] = None
        if self._allowed_content is not None:
            arg_order.append('content')
            arg_value['content'] = None

        for key in kwargs:
            if key in arg_order:
                arg_value[key] = kwargs[key]
                # now delete key from arg_order and kwargs
                arg_order.remove(key)
                del kwargs[key]

        # now check if content has been filled, if not, search for a list
        if self._allowed_content is not None:
            if arg_value['content'] is None:
                for item in args:
                    if isinstance(item, list):
                        arg_value['content'] = item
                        arg_order.remove('content')
                        args.remove(item)
                        break

        # loop over left-over positional arguments
        for item in args:
            if len(arg_order) > 0:
                arg_value[arg_order[0]] = item
                del arg_order[0]
            else:
                # we ran out of arguments to store this stuff in
                raise InvalidArgument(
                    "got more arguments than allowed: %r" % item)

        # validate arguments
        for arg in self._arguments:
            if arg_value[arg.name] is None and not arg.optional:
                raise InvalidArgument(
                    "%s argument is not optional" % arg.name)
            elif arg.type_ is None:
                # Unimplemented type, issue warning, accept any value
                pass
            elif isinstance(arg.type_, tuple):
                # TODO: do a typecheck on value
                pass
            else:
                if not isinstance(arg_value[arg.name], arg.type_):
                    raise InvalidArgument(
                        "Expected %r, got %r" % (
                            arg.type_,
                            arg_value[arg.name]))
            # now we're sure this is a valid argument, store it
            self._stored_arguments[arg.name] = arg_value[arg.name]

        # handle position (optional)
        if 'attachment' in self._types:
            if arg_value['position'] is not None:
                self._position = arg_value['position']

        # handle content (optional)
        if self._allowed_content is not None:
            self._content = []
            if arg_value['content'] is not None:
                for item in arg_value['content']:
                    # TODO: do a type check on content
                    # for now we accept anything
                    self._content.append(item)

    def __format__(self, format_spec):
        """Return lilypond code."""
        indent_level = 0
        if format_spec != "":
            indent_level = int(format_spec)
        result = "%s%s" % (self._position, self._tag)
        if len(self._stored_arguments) > 0:
            result += " " + " ".join(
                format(self._stored_arguments[key])
                for key in self._stored_arguments)
        # now handle contents!
        if self._allowed_content is not None:
            result += " %s" % self._delimiter_open
            if len(self._content) == 0:
                # directly close, no newline!
                result += " %s" % self._delimiter_close
            elif len(self._content) == 1:
                # keep it on the same rule
                result += " %s %s" % (
                    format(self._content[0], str(indent_level)),
                    self._delimiter_close)
            else:
                # more than one item, start newline and indent stuff
                # TODO: handle formatting of more that one item
                pass
        return result
