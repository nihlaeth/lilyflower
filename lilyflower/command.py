"""Non-container command."""
from errors import InvalidArgument


class Command(object):

    """Non-container command."""

    command = ""
    min_args = 0
    max_args = 0
    newline = True

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
        result = "%s%s%s%s" % (
            "  " * indent_level,
            self.command,
            " " + " ".join(
                format(item, str(indent_level + 1)) for item in self.args),
            ("\n" if self.newline else ""))
        return result
