"""Container type - can contain leafs and other containers."""


class Container(object):

    """Contain leafs and other containers."""

    def __init__(self, contents, arguments=None):
        """
        Create container.

        contents -> (list) objects that make up the contents of container
        arguments -> (list) depending on subclass, this container
            might require arguments, or have optional arguments.
        """
        self.command = ""
        if arguments is None:
            self.arguments = []
        else:
            self.arguments = arguments
        self.delimiter_pre = "{"
        self.delimiter_post = "}"
        self.container = contents

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

    def __delitem__(self, index, value):
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
        return " ".join(format(self.arguments))

    def __format__(self, format_spec):
        """Return lilypond code."""
        indent_level = 0
        if format_spec is not "":
            indent_level = int(format_spec)
        result = "\n%s" % ("  " * indent_level)
        if self.command != "":
            result += "%s %s %s\n" % (
                self.command,
                self._format_arguments(),
                self.delimiter_pre)
        else:
            result += "%s\n" % self.delimiter_pre

        result += "  " * (indent_level + 1)
        for item in self.container:
            if isinstance(item, Container):
                result += format(
                    item,
                    str(indent_level + 1))
            else:
                result += "%s " % format(item)
        result += "\n%s%s\n" % ("  " * indent_level, self.delimiter_post)

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
