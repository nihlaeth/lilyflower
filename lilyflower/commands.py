"""Non-container commands."""
from command import Command
from errors import InvalidArgument


class Bar(Command):

    """Bar checks and delimiters."""

    command = "\\bar"
    min_arguments = 1
    max_arguments = 1
    inline = True

    def validate_arguments(self):
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
        if self.arguments[0] not in valid_bars:
            raise InvalidArgument(
                "%s not a valid bar type." % self.arguments[0])
        else:
            self.validated_arguments = ["\"%s\"" % self.arguments[0]]
