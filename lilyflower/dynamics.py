"""Dynamic commands."""
# pylint: disable=too-few-public-methods
from lilyflower.notecommands import NoteCommand
from lilyflower.errors import InvalidArgument


class Dynamic(NoteCommand):

    """Dynamic mark."""

    _inline = True


class Crescendo(Dynamic):

    r"""
    A crescendo.

    First format(), it displays \\>, the second time it displays the
    defined close command (see below).

    Optional argument: closing part (Dynamic) - default = \\!
    """

    _command = "\\<"
    _close = "\\!"
    _max_arguments = 1
    _num_displays = 0

    def _validate_arguments(self):
        """Set the closing part."""
        if len(self._arguments) == 1:
            if not isinstance(self._arguments[0], Dynamic):
                raise InvalidArgument("Expects a Dynamic as closing part.")
            else:
                self._close = self._arguments[0]

    def __format__(self, _):
        """Return lilypond code."""
        if self._num_displays % 2 == 0:
            self._num_displays += 1
            return self._command
        elif self._num_displays % 2 == 1:
            self._num_displays += 1
            return format(self._close)


class Decrescendo(Crescendo):

    r"""
    A decrescendo.

    First format(), it displays \\>, the second time it displays the
    defined close _command (see below).

    Optional argument: closing part (Dynamic) - default = \\!
    """

    _command = "\\>"


class Piano5(Dynamic):

    r"""Pianississississimo (\\ppppp)."""

    _command = "\\ppppp"


class Piano4(Dynamic):

    r"""Pianissississimo (\\pppp)."""

    _command = "\\pppp"


class Piano3(Dynamic):

    r"""Pianississimo (\\ppp)."""

    _command = "\\ppp"


class Piano2(Dynamic):

    r"""Pianissimo (\\pp)."""

    _command = "\\pp"


class Piano(Dynamic):

    r"""Piano (\\p)."""

    _command = "\\p"


class MezzoPiano(Dynamic):

    r"""MezzoPiano (\\mp)."""

    _command = "\\mp"


class MezzoForte(Dynamic):

    r"""MezzoForte (\\mf)."""

    _command = "\\mf"


class Forte(Dynamic):

    r"""Forte (\\f)."""

    _command = "\\f"


class Forte2(Dynamic):

    r"""Fortissimo (\\ff)."""

    _command = "\\ff"


class Forte3(Dynamic):

    r"""Fortississimo (\\fff)."""

    _command = "\\fff"


class Forte4(Dynamic):

    r"""Fortissississimo (\\ffff)."""

    _command = "\\ffff"


class Forte5(Dynamic):

    r"""Fortississississimo (\\fffff)."""

    _command = "\\fffff"


class FortePiano(Dynamic):

    r"""FortePiano (\\fp)."""

    _command = "\\fp"


class Sforzato(Dynamic):

    r"""Sforzato (\\sf)."""

    _command = "\\sf"


class Sfortissimo(Dynamic):

    r"""No idea what this is called properly (\\sff)."""

    _command = "\\sff"


class Sforzando(Dynamic):

    r"""Sforzando (\\sfz)."""

    _command = "\\sfz"


class Spiano(Dynamic):

    r"""No idea what this is called properly (\\sp)."""

    _command = "\\sp"


class Spianissimo(Dynamic):

    r"""No idea what this is called properly (\\spp)."""

    _command = "\\spp"


class Rinforzando(Dynamic):

    r"""Rinforzando (\\rfz)."""

    _command = "\\rfz"
