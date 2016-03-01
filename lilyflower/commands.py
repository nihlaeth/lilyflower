"""Non-container commands."""
from command import Command
from errors import InvalidArgument


class Bar(Command):

    """Bar checks and delimiters."""

    command = "\\bar"
    min_args = 1
    max_args = 1
    newline = False

    def validate_args(self):
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
        if self.args[0] not in valid_bars:
            raise InvalidArgument("%s not a valid bar type." % self.args[0])
