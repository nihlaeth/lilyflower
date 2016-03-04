"""Dynamic commands."""
# pylint: disable=relative-import,too-few-public-methods
from notecommands import NoteCommand
from errors import InvalidArgument


class Dynamic(NoteCommand):

    """Dynamic mark."""

    inline = True


class Crescendo(Dynamic):

    r"""
    A crescendo.

    First format(), it displays \\>, the second time it displays the
    defined close command (see below).

    Optional argument: closing part (Dynamic) - default = \\!
    """

    command = "\\<"
    close = "\\!"
    max_arguments = 1
    num_displays = 0

    def validate_arguments(self):
        """Set the closing part."""
        if len(self.arguments) == 1:
            if not isinstance(self.arguments[0], Dynamic):
                raise InvalidArgument("Expects a Dynamic as closing part.")
            else:
                self.close = self.arguments[0]

    def __format__(self, _):
        """Return lilypond code."""
        if self.num_displays % 2 == 0:
            self.num_displays += 1
            return self.command
        elif self.num_displays % 2 == 1:
            self.num_displays += 1
            return format(self.close)


class Decrescendo(Crescendo):

    r"""
    A decrescendo.

    First format(), it displays \\>, the second time it displays the
    defined close command (see below).

    Optional argument: closing part (Dynamic) - default = \\!
    """

    command = "\\>"


class Piano5(Dynamic):

    r"""Pianississississimo (\\ppppp)."""

    command = "\\ppppp"


class Piano4(Dynamic):

    r"""Pianissississimo (\\pppp)."""

    command = "\\pppp"


class Piano3(Dynamic):

    r"""Pianississimo (\\ppp)."""

    command = "\\ppp"


class Piano2(Dynamic):

    r"""Pianissimo (\\pp)."""

    command = "\\pp"


class Piano(Dynamic):

    r"""Piano (\\p)."""

    command = "\\p"


class MezzoPiano(Dynamic):

    r"""MezzoPiano (\\mp)."""

    command = "\\mp"


class MezzoForte(Dynamic):

    r"""MezzoForte (\\mf)."""

    command = "\\mf"


class Forte(Dynamic):

    r"""Forte (\\f)."""

    command = "\\f"


class Forte2(Dynamic):

    r"""Fortissimo (\\ff)."""

    command = "\\ff"


class Forte3(Dynamic):

    r"""Fortississimo (\\fff)."""

    command = "\\fff"


class Forte4(Dynamic):

    r"""Fortissississimo (\\ffff)."""

    command = "\\ffff"


class Forte5(Dynamic):

    r"""Fortississississimo (\\fffff)."""

    command = "\\fffff"


class FortePiano(Dynamic):

    r"""FortePiano (\\fp)."""

    command = "\\fp"


class Sforzato(Dynamic):

    r"""Sforzato (\\sf)."""

    command = "\\sf"


class Sfortissimo(Dynamic):

    r"""No idea what this is called properly (\\sff)."""

    command = "\\sff"


class Sforzando(Dynamic):

    r"""Sforzando (\\sfz)."""

    command = "\\sfz"


class Spiano(Dynamic):

    r"""No idea what this is called properly (\\sp)."""

    command = "\\sp"


class Spianissimo(Dynamic):

    r"""No idea what this is called properly (\\spp)."""

    command = "\\spp"


class Rinforzando(Dynamic):

    r"""Rinforzando (\\rfz)."""

    command = "\\rfz"
