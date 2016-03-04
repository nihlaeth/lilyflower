"""Container type - can contain leafs and other containers."""
from lilyflower.errors import InvalidArgument


class Container(object):

    r"""
    Main structural component.

    Every container type command inherits from this.

    Iterable / sequence type.

    Use format() to get lilypond code.

    Usage::

        Container(content, arguments=None)

    Parameters
    ==========
    content: list, lilyflower object
        contents of the container. Subclasses can set stricter requirements.
    arguments: list, optional
        arguments for this container. Container does not accept any
        arguments, subclasses set their own requirements.

    Returns
    =======
    None

    Raises
    =======
    InvalidArgument:
        when too many, too little, or the wrong type arguments are provided
        (subclasses decide what's valid)
    InvalidContent:
        when the wrong content type is provided (subclasses determine
        what's valid)

    Notes
    =====
    A container with length zero will display delimiters (curly braces
    in most cases), so will a container with length >= 2. A container
    with a single item in it however (regardless if that's a container
    or not), will forego delimiters.

    Examples
    ========

    .. testsetup::

        from lilyflower.container import Container
        from lilyflower.tones import Note

    .. doctest::

        >>> container = Container([])
        >>> print format(container)
        {
        }
        >>> container.append(Note('a'))
        >>> print format(container)
        a
        >>> container += Note('b')
        >>> print format(container)
        {
          a b
        }
        >>> container[1] = Container([Note('b'), Note('c')])
        >>> print format(container)
        {
          a
          {
            b c
          }
        }
        >>> container.extend([Container([]), Container([Note('d'), Note('e')])])
        >>> print format(container)
        {
          a
          {
            b c
          }
          {
          }
          {
            d e
          }
        }
        >>> container = Container([Note('a'), Note('b'), Note('c')])
        >>> for item in container:
        ...     print format(item)
        a
        b
        c
        >>> container[2] = Container([Note('c'), Note('d'), Note('e')])
        >>> container.reverse()
        >>> print format(container)
        {
          {
            e d c
          }
          b a
        }
    """

    _command = ""
    _delimiter_pre = "{"
    _delimiter_post = "}"
    _min_arguments = 0
    _max_arguments = 0
    _validated_arguments = None
    _inline = False

    def __init__(self, content, arguments=None):
        """
        Create container.

        content -> (list) objects that make up the content of container
        arguments -> (list) depending on subclass, this container
            might require arguments, or have optional arguments.
        """
        self._container = content
        self._validate_content()
        self._validated_arguments = []
        # deal with arguments
        if arguments is None:
            self._arguments = []
        else:
            self._arguments = arguments
        if len(self._arguments) < self._min_arguments or \
                len(self._arguments) > self._max_arguments:
            raise InvalidArgument("Expects between %d and %d arguments." % (
                self._min_arguments,
                self._max_arguments))
        self._validate_arguments()

    def _validate_content(self):
        """
        Do some in-depth content validation.

        This method is a placeholder to be overwritten by child
        classes.
        """
        pass

    def _validate_arguments(self):
        """
        Do some in-depth argument validation.

        This method is meant to be overwritten, so child
        classes can validate beyond number of arguments with
        little duplicate code.

        Note: this method should not return anything. If something's
        up, raise an exception.

        Side effect: it puts validated arguments in self._validated_arguments
        """
        pass

    def append(self, value):
        """Add to the end of the container."""
        self._container.append(value)

    def extend(self, extension):
        """Add list to end of container."""
        self._container.extend(extension)

    def insert(self, index, value):
        """Insert value at index."""
        self._container.insert(index, value)

    def count(self, value):
        """Count occurances of value."""
        # TODO: provide a more useful implementation that looks inside items
        return self._container.count(value)

    def pop(self):
        """Pop value."""
        return self._container.pop()

    def remove(self, value):
        """Remove first occurenc of value."""
        self._container.remove(value)

    def reverse(self):
        """Reverse order."""
        self._container.reverse()
        # now reverse all containers inside this one as well
        for item in self._container:
            if isinstance(item, Container):
                item.reverse()

    def sort(self, cmp=None, key=None, reverse=False):
        """Sort container."""
        self._container.sort(cmp, key, reverse)

    def index(self, value):
        """Find index of value in container."""
        return self._container.index(value)

    def __iter__(self):
        """Return iterator object."""
        return iter(self._container)

    def __reversed__(self):
        """Iterate over object in reverse order (UNIMPLEMENTED)."""
        pass

    def __getitem__(self, index):
        """Return item at index."""
        return self._container[index]

    def __setitem__(self, index, value):
        """Set item at index."""
        self._container[index] = value

    def __delitem__(self, index):
        """Delete item at index."""
        del self._container[index]

    def __len__(self):
        """Return length of container."""
        return len(self._container)

    def _format_arguments(self):
        """
        Format arguments.

        Subclass overwrites this if there are any required
        arguments. Otherwise it assumes the order given is fine.
        """
        result = ""
        for argument in self._validated_arguments:
            result += format(argument) + " "
        return result

    def __format__(self, format_spec):
        """Return lilypond code."""
        indent_level = 0
        if format_spec is not "":
            indent_level = int(format_spec)
        if len(self._container) == 1:
            # don't print delimiters at length 1
            # also, don't increase indent, we didn't use it here
            if self._command == "":
                return format(self._container[0], str(indent_level))
            elif len(self._validated_arguments) == 0:
                return "%s %s" % (
                    self._command,
                    format(self._container[0], str(indent_level)))
            else:
                return "%s %s %s" % (
                    self._command,
                    self._format_arguments(),
                    format(self._container[0], str(indent_level)))
        result = ""
        if self._command != "":
            result += "%s %s%s" % (
                self._command,
                self._format_arguments(),
                self._delimiter_pre)
        else:
            result += self._delimiter_pre

        inline_previous = False
        for item in self._container:
            separator = "\n%s" % ("  " * (indent_level + 1))
            inline_current = item._inline
            # the only time we need a space as separator is
            # when both the current and previous item are inline
            if inline_previous and inline_current:
                separator = " "
            result += "%s%s" % (separator, format(
                item,
                str(indent_level + 1)))
            inline_previous = inline_current
        result += "\n%s%s" % ("  " * indent_level, self._delimiter_post)

        return result

    def __iadd__(self, other):
        """Add something to the container in place."""
        if isinstance(other, Container):
            self.extend(other.container)
        elif isinstance(other, list):
            self.extend(other)
        else:
            # assume other is a single object or value
            self.append(other)
        return self

    def __add__(self, other):
        """Add something to the container."""
        # Since we're not creating a new object, this is the same
        # as __iadd__()
        return self.__iadd__(other)

    def __radd__(self, other):
        """Add something to the container - arguments reversed."""
        # Same thing as add.
        return self.__add__(other)

    def __imul__(self, other):
        """Multiply container in place."""
        # Other has to be an integer
        if not isinstance(other, int):
            raise TypeError
        self._container *= other
        return self

    def __mul__(self, other):
        """Multiply container."""
        # Same thing as __imul__()
        return self.__imul__(other)

    def __rmul__(self, other):
        """Multiply conainer, arguments reversed."""
        # Same thing as __mul__()
        return self.__mul__(other)
