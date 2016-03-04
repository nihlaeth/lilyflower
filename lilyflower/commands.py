"""Non-container commands."""
from lilyflower.command import Command
from lilyflower.errors import InvalidArgument


class Bar(Command):

    """Bar checks and delimiters."""

    _command = "\\bar"
    _min_arguments = 1
    _max_arguments = 1
    _inline = True

    def _validate_arguments(self):
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
        if self._arguments[0] not in valid_bars:
            raise InvalidArgument(
                "%s not a valid bar type." % self._arguments[0])
        else:
            self._validated_arguments = ["\"%s\"" % self._arguments[0]]
