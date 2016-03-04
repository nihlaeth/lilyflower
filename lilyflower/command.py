"""Non-container command."""
from errors import InvalidArgument


class Command(object):

    """Non-container command."""

    command = ""
    min_arguments = 0
    max_arguments = 0
    inline = False
    validated_arguments = None

    def __init__(self, *arguments):
        """Store arguments."""
        if len(arguments) < self.min_arguments or \
                len(arguments) > self.max_arguments:
            raise InvalidArgument("Expects between %d and %d arguments." % (
                self.min_arguments, self.max_arguments))
        self.arguments = arguments
        self.validate_arguments()

    def validate_arguments(self):
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
        result = self.command
        if self.validated_arguments is not None:
            new_indent = indent_level + 1
            result += " " + " ".join(
                format(
                    item,
                    str(new_indent)) for item in self.validated_arguments)
        return result
