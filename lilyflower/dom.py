"""All the lilypond elements."""
import datetime
import re
from lilyflower.syntax import SPEC
from lilyflower.node import Node
from lilyflower.tools import property_to_class, generate_docstring
from lilyflower.errors import InvalidArgument

for key in SPEC:
    class_name = property_to_class(key)
    attributes = SPEC[key]
    globals()[class_name] = type(
        class_name,
        (Node,),
        {
            '__doc__': generate_docstring(class_name, attributes),
            '_tag': attributes.lily_name,
            '_types': attributes.types,
            '_arguments': attributes.arguments,
            '_allowed_content': attributes.allowed_content,
            '_inline': attributes.inline,
            '_delimiter_open': attributes.delimiter_open,
            '_delimiter_close': attributes.delimiter_close})


class LilyFile(Node):

    r"""
    Base of the lilypond object tree.

    Unlike other `Node` subclasses, `LilyFile` does not indent its
    contents, nor does it have a delimiter. It adds some information
    to the top (lilypond version and a comment with creation info).

    Usage:

        `LilyFile(content=None, version=None)`

    Parameters
    ==========
    content: list, music expression, optional
        List of Node objects with type music
    version: string, optional
        Lilypond version this code is written for (default=2.18.2)

    Raises
    ======
    InvalidArgument:
        if version is not a valid version identifier
    InvalidContent:
        if any of the content items is not a music expression

    See Also
    ========
    :class:`lilyflower.node.Node`
    :class:`lilyflower.errors.InvalidArgument`
    :class:`lilyflower.errors.InvalidContent`

    Examples
    ========
    .. testsetup::

        from lilyflower.dom import LilyFile, Score

    .. doctest::

        >>> print format(LilyFile([Score()], version="2.18.2"))
        % Created with lilyflower at ...-...-... ...:...:...
        \version 2.18.2
        <BLANKLINE>
        \score { }
    """

    def __init__(self, content=None, version=None):
        """Set content and version."""
        self._content = []
        if content is not None:
            for item in content:
                # TODO: validate content
                pass
            self._content += content
        if version is None:
            version = "2.18.2"
        if re.match(r"^[0-9]+[0-9\.]*$", version) is None:
            raise InvalidArgument("%r not a valid version string" % version)
        else:
            self._version = version

    def __format__(self, _):
        """Return lilypond code."""
        result = "%% Created with lilyflower at %s\n" % datetime.datetime.now()
        result += "\\version %s\n\n" % self._version
        result += "\n".join(format(item) for item in self._content)
        return result
