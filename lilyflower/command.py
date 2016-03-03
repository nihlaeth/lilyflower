"""Non-container command."""
from errors import InvalidArgument


class Command(object):

    """Non-container command."""

    command = ""
    min_args = 0
    max_args = 0
    inline = False
    validated_arguments = None

    def __init__(self, *args):
        """Store arguments."""
        if len(args) < self.min_args or len(args) > self.max_args:
            raise InvalidArgument("Expects between %d and %d arguments." % (
                self.min_args, self.max_args))
        self.args = args
        self.validate_args()

    def validate_args(self):
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
        result = "%s%s" % (
            "  " * indent_level,
            self.command)
        if self.validated_arguments is not None:
            new_indent = indent_level + 1
            result += " " + " ".join(
                format(
                    item,
                    str(new_indent)) for item in self.validated_arguments)
        return result
