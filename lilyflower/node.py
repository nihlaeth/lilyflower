"""Basic building block for the object tree."""
from collections import OrderedDict
import re
from lilyflower.errors import InvalidArgument, InvalidContent
from lilyflower.tools import compare_iter


# pylint: disable=protected-access
# We only access protected content of our own children,
# content needs to stay protected for end user.
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
    .. testsetup::

        from lilyflower.node import Node

    .. doctest::

        >>> node = Node([Node(), Node(), Node()])
        >>> for item in node:
        ...     print format(item)
        { }
        { }
        { }
        >>> node.append(Node())
        >>> print len(node)
        4

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
            self._validate_argument(arg.name, arg_value[arg.name])
            # now we're sure this is a valid argument, store it
            self._stored_arguments[arg.name] = arg_value[arg.name]

        # handle position (optional)
        if 'attachment' in self._types:
            if arg_value['position'] is not None:
                self._validate_argument('position', arg_value['position'])
                self._position = arg_value['position']

        # handle content (optional)
        if self._allowed_content is not None:
            self._content = []
            if arg_value['content'] is not None:
                for item in arg_value['content']:
                    self._validate_content(item)
                    self._content.append(item)

    def _validate_content(self, item):
        """Validate content item."""
        if not isinstance(item, Node):
            raise InvalidContent("%r not a Node object." % item)
        if not compare_iter(self._allowed_content, item._types):
            raise InvalidContent("Type mismatch: %r, %r" % (
                self._allowed_content,
                item._types))
        return True

    def _validate_argument(self, name, value):
        """Validate argument."""
        # special arguments (position)
        if name == 'position':
            if re.match(r"^[\^\-_]?$", value) is None:
                raise InvalidArgument("%r is not a valid position" % value)
            else:
                return True

        # fetch argument
        arg = None
        for item in self._arguments:
            if item.name == name:
                arg = item
        if arg is None:
            InvalidArgument('%r: no such argument' % name)
        elif arg.type_ is None:
            # Unimplemented type, issue warning, accept any value
            return True
        elif isinstance(arg.type_, tuple):
            if not isinstance(value, Node):
                raise InvalidArgument("Expected Node for %s, not %r" % (
                    name,
                    value))
            if not compare_iter(arg.type_, value._types):
                raise InvalidArgument(
                    "Type mismatch: %r, %r" % (arg.type_, value._types))
        else:
            if not isinstance(value, arg.type_):
                raise InvalidArgument(
                    "Expected %r, got %r" % (
                        arg.type_,
                        value))
        return True

    def append(self, value):
        """Add item to the end of content."""
        if self._allowed_content is not None:
            self._validate_content(value)
            self._content.append(value)
        else:
            raise ValueError("%s has no content" % self._tag)

    def extend(self, extension):
        """Add iterable to end of container (another Node for example)."""
        if self._allowed_content is not None:
            for item in extension:
                self.append(item)
        else:
            raise ValueError("%s has no content" % self._tag)

    def insert(self, index, value):
        """Insert value into content at index."""
        if self._allowed_content is not None:
            self._validate_content(value)
            self._content.insert(index, value)
        else:
            raise ValueError("%s has no content" % self._tag)

    def count(self, value):
        """Count occurances of value in content."""
        if self._allowed_content is not None:
            return self._content.count(value)
        else:
            raise ValueError("%s has no content" % self._tag)

    def pop(self):
        """Pop value from content."""
        if self._allowed_content is not None:
            return self._content.pop()
        else:
            raise ValueError("%s has no content" % self._tag)

    def remove(self, value):
        """Remove first occurance of value from content."""
        if self._allowed_content is not None:
            self._content.remove(value)
        else:
            raise ValueError("%s has no content" % self._tag)

    def reverse(self, depth=-1):
        """Reverse order of content and that of children to depth."""
        if self._allowed_content is not None and depth != 0:
            self._content.reverse()
            for item in self._content:
                item.reverse(depth - 1)

    def sort(self, cmp=None, key=None, reverse=False, depth=-1):
        """Sort content to depth."""
        if self._allowed_content is not None and depth != 0:
            self._content.sort(cmp, key, reverse)
            for item in self._content:
                item.sort(cmp, key, reverse, depth - 1)

    def index(self, value):
        """Find index of value in content."""
        if self._allowed_content is not None:
            return self._content.index(value)
        else:
            raise ValueError("%s has no content" % self._tag)

    def __getitem__(self, name):
        """
        Get item from content or arguments.

        if `name` is `str`: return from `self._stored_arguments`
        if `name` is `int`: return from `self._content`
        """
        if isinstance(name, basestring):
            return self._stored_arguments[name]
        elif isinstance(name, int) or isinstance(name, slice):
            return self._content[name]
        else:
            raise NameError("%r is not a valid key" % name)

    def __setitem__(self, name, value):
        """
        Set item in content or arguments.

        if `name` is `str`: set item in `self._stored_arguments`
        if `name` is `int` or `slice`: set item in `self._content`
        """
        if isinstance(name, basestring):
            self._validate_argument(name, value)
            self._stored_arguments[name] = value
        elif isinstance(name, int) or isinstance(name, slice):
            self._validate_content(value)
            self._content[name] = value
        else:
            raise NameError("%r is not a valid key" % name)

    def __delitem__(self, name):
        """
        Delete item from content or arguments.

        if `name` is `str`: del item in `self._stored_arguments`
        if `name` is `int` or `slice`: del item in `self._content`
        """
        if isinstance(name, basestring):
            del self._stored_arguments[name]
        elif isinstance(name, int) or isinstance(name, slice):
            del self._content[name]
        else:
            raise NameError("%r is not a valid key" % name)

    def __len__(self):
        """Return length of content."""
        if self._allowed_content is not None:
            return len(self._content)
        else:
            return 0

    def __iter__(self):
        """Return iterable for content."""
        if self._allowed_content is not None:
            return iter(self._content)
        else:
            raise StopIteration

    def __reversed__(self):
        """Return iterable for backwards iteration over content."""
        if self._allowed_content is not None:
            return iter(self._content[::-1])
        else:
            raise StopIteration

    def iter_depth(self, depth=-1):
        """Iterate over children and their contents, limited by depth."""
        if depth != 0:
            for child in self:
                yield child
                for child_content in child.iter_depth(depth - 1):
                    yield child_content
        else:
            raise StopIteration

    def __format__(self, format_spec):
        """Return lilypond code."""
        indent_level = 0
        if format_spec != "":
            indent_level = int(format_spec)
        result = "%s%s" % (self._position, self._tag)
        if len(self._stored_arguments) > 0:
            result += " %s%s" % (
                " ".join(
                    format(self._stored_arguments[key])
                    for key in self._stored_arguments),
                " " if self._allowed_content is not None else "")
        if len(self._stored_arguments) == 0 and \
                self._allowed_content is not None and \
                self._tag is not "":
            result += " "

        # now handle content!
        if self._allowed_content is not None:
            result += "%s" % self._delimiter_open
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
                inline_previous = False
                for item in self._content:
                    separator = "\n%s" % ("  " * (indent_level + 1))
                    inline_current = item._inline
                    # the only time when we need a space as a
                    # separator is when both the current and
                    # previous item are inline
                    if inline_previous and inline_current:
                        separator = " "
                    result += "%s%s" % (separator, format(
                        item,
                        str(indent_level + 1)))
                    inline_previous = inline_current
                result += "\n%s%s" % (
                    "  " * indent_level,
                    self._delimiter_close)

        return result
