"""Container type - can contain leafs and other containers."""
from errors import InvalidArgument


class Container(object):

    """Contain leafs and other containers."""

    command = ""
    delimiter_pre = "{"
    delimiter_post = "}"
    min_arguments = 0
    max_arguments = 0
    validated_arguments = None
    inline = False

    def __init__(self, content, arguments=None):
        """
        Create container.

        content -> (list) objects that make up the content of container
        arguments -> (list) depending on subclass, this container
            might require arguments, or have optional arguments.
        """
        self.container = content
        self.validate_content()
        self.validated_arguments = []
        # deal with arguments
        if arguments is None:
            self.arguments = []
        else:
            self.arguments = arguments
        if len(self.arguments) < self.min_arguments or \
                len(self.arguments) > self.max_arguments:
            raise InvalidArgument("Expects between %d and %d arguments." % (
                self.min_arguments,
                self.max_arguments))
        self.validate_arguments()

    def validate_content(self):
        """
        Do some in-depth content validation.

        This method is a placeholder to be overwritten by child
        classes.
        """
        pass

    def validate_arguments(self):
        """
        Do some in-depth argument validation.

        This method is meant to be overwritten, so child
        classes can validate beyond number of arguments with
        little duplicate code.

        Note: this method should not return anything. If something's
        up, raise an exception.

        Side effect: it puts validated arguments in self.validated_arguments
        """
        pass

    def append(self, value):
        """Add to the end of the container."""
        self.container.append(value)

    def extend(self, extension):
        """Add list to end of container."""
        self.container.extend(extension)

    def insert(self, index, value):
        """Insert value at index."""
        self.container.insert(index, value)

    def count(self, value):
        """Count occurances of value."""
        # TODO: provide a more useful implementation that looks inside items
        return self.container.count(value)

    def pop(self):
        """Pop value."""
        return self.container.pop()

    def remove(self, value):
        """Remove first occurenc of value."""
        self.container.remove(value)

    def reverse(self):
        """Reverse order."""
        # TODO: preserve meaning and correct syntax when reversing
        self.container.reverse()

    def sort(self, cmp=None, key=None, reverse=False):
        """Sort container."""
        self.container.sort(cmp, key, reverse)

    def index(self, value):
        """Find index of value in container."""
        return self.container.index(value)

    def __iter__(self):
        """Return iterator object."""
        return iter(self.container)

    def __reversed__(self):
        """Iterate over object in reverse order."""
        pass

    def __getitem__(self, index):
        """Return item at index."""
        return self.container[index]

    def __setitem__(self, index, value):
        """Set item at index."""
        self.container[index] = value

    def __delitem__(self, index):
        """Delete item at index."""
        del self.container[index]

    def __len__(self):
        """Return length of container."""
        return len(self.container)

    def _format_arguments(self):
        """
        Format arguments.

        Subclass overwrites this if there are any required
        arguments. Otherwise it assumes the order given is fine.
        """
        # TODO: support for indents, so \with blocks are indented properly
        result = ""
        for argument in self.validated_arguments:
            result += format(argument) + " "
        return result

    def __format__(self, format_spec):
        """Return lilypond code."""
        indent_level = 0
        if format_spec is not "":
            indent_level = int(format_spec)
        if len(self.container) == 1:
            # don't print delimiters at length 1
            # also, don't increase indent, we didn't use it here
            if self.command == "":
                return format(self.container[0], str(indent_level))
            elif len(self.validated_arguments) == 0:
                return "%s %s" % (
                    self.command,
                    format(self.container[0], str(indent_level)))
            else:
                return "%s %s %s" % (
                    self.command,
                    self._format_arguments(),
                    format(self.container[0], str(indent_level)))
        result = ""
        if self.command != "":
            result += "%s %s%s" % (
                self.command,
                self._format_arguments(),
                self.delimiter_pre)
        else:
            result += self.delimiter_pre

        inline_previous = False
        for item in self.container:
            separator = "\n%s" % ("  " * (indent_level + 1))
            inline_current = item.inline
            # the only time we need a space as separator is
            # when both the current and previous item are inline
            if inline_previous and inline_current:
                separator = " "
            result += "%s%s" % (separator, format(
                item,
                str(indent_level + 1)))
            inline_previous = inline_current
        result += "\n%s%s" % ("  " * indent_level, self.delimiter_post)

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
        self.container *= other
        return self

    def __mul__(self, other):
        """Multiply container."""
        # Same thing as __imul__()
        return self.__imul__(other)

    def __rmul__(self, other):
        """Multiply conainer, arguments reversed."""
        # Same thing as __mul__()
        return self.__mul__(other)
