"""Some tools."""
import re
from lilyflower.schemedata import (
    String,
    SignedInt,
    UnsignedInt,
    SignedFloat,
    UnsignedFloat,
    Axis,
    Direction,
    Symbol,
    Procedure,
    Color,
    Pair,
    List,
    AssociationList,
    Boolean)
from lilyflower.errors import InvalidArgument


def compare_iter(one, two):
    r"""
    Compare two iterables to see if they have any elements in common.

    Examples
    ========
    .. testsetup::

        from lilyflower.tools import compare_iter

    .. doctest::

        >>> compare_iter((0, 1, 2), (3, 4, 5))
        False
        >>> compare_iter((0, 1, 3), (3,))
        True
        >>> compare_iter([1, 3, 5], ())
        False
        >>> compare_iter([], ())
        True
    """
    if len(one) == 0 and len(two) == 0:
        # special case - supported for testing Node
        return True
    for item in one:
        if item in two:
            return True
    return False


def property_to_class(name):
    r"""Convert property name to class name.

    Examples
    ========
    .. testsetup::

        from lilyflower.dom import property_to_class

    .. doctest::

        >>> print property_to_class('test_me')
        TestMe
        >>> print property_to_class('nounderscores')
        Nounderscores
        >>> print property_to_class('lots_of_underscores_here')
        LotsOfUnderscoresHere

    """
    # trick re into making the first character uppercase as well
    name = "_" + name
    return re.sub(
        "_(?P<first>[a-z])",
        lambda m: m.group('first').upper(),
        name)


def generate_docstring(class_name, attributes):
    """Generate docstring for programatically generated node children."""
    title = "%s (%r) %s." % (
        class_name,
        attributes.lily_name,
        "command" if attributes.allowed_content is None else "container")
    args = ", ".join([item.name for item in attributes.arguments])

    docstring = """
    {title}

    Usage:
        {name}({args})

    Parameters
    ==========""".format(title=title, name=class_name, args=args)

    for arg in attributes.arguments:
        # TODO: give meaningful information about the different types
        if arg.type_ is not None:
            types = str(arg.type_)
        else:
            types = "UNIMPLEMENTED"
        docstring += "\n    %s: %s" % (arg.name, types)
        if arg.optional:
            docstring += ", optional"
        # TODO: give a bit more text to a parameter
    # TODO: add position parameter if attachment (also in usage)
    # TODO: add content parameter if container (also in usage)

    docstring += """

    Returns
    =======
    `None`

    Raises
    ======
    lilyflower.errors.InvalidArgument:
        if any of the arguments doesn't match the type requirement,
        or if there are too many or too few arguments.
    """
    if attributes.allowed_content is not None:
        docstring += """lilyflower.errors.InvalidContent:
        if any of the content does not match the type requirement.
    """

    docstring += """
    Notes
    =====
    """
    # TODO: add some useful notes on parameter resolve order

    docstring += """

    See Also
    ========
    :class:`lilyflower.node.Node`
    :class:`lilyflower.errors.InvalidArgument`
    """

    if attributes.allowed_content is not None:
        docstring += """:class:`lilyflower.errors.InvalidContent`
    """

    imports_scheme = []
    imports_this = [class_name]
    args = []
    for arg in attributes.arguments:
        # Note: the matching order matters, because of inheritance within
        # lilyflower.schemedata
        if arg.type_ is None:
            # Unimplemented type
            # TODO: issue warning about unimplemented type
            pass
        elif isinstance(arg.type_, tuple):
            # list of node types allowed as argument
            if 'markup' in arg.type_:
                imports_this.append("Bold")
                # we can't import Bold for real because of circular
                # dependencies
                args.append(("Bold([])", r"\bold { }"))
            # TODO: handle other argument types (like 'music')
        elif issubclass(arg.type_, String):
            imports_scheme.append("String")
            args.append(("String('test')", String("test")))
        elif issubclass(arg.type_, Direction):
            imports_scheme.append("Direction")
            args.append(("Direction('up')", Direction('up')))
        elif issubclass(arg.type_, Axis):
            imports_scheme.append("Axis")
            args.append(("Axis('x')", Axis('x')))
        elif issubclass(arg.type_, SignedFloat):
            imports_scheme.append("SignedFloat")
            args.append(("SignedFloat(0)", SignedFloat(0)))
        elif issubclass(arg.type_, Color):
            imports_scheme.append("Color")
            args.append(("Color('blue')", Color('blue')))
        elif issubclass(arg.type_, Boolean):
            imports_scheme.append("Boolean")
            args.append(("Boolean(True)", Boolean(True)))
        elif issubclass(arg.type_, UnsignedInt):
            imports_scheme.append("UnsignedInt")
            args.append(("UnsignedInt(0)", UnsignedInt(0)))
        elif issubclass(arg.type_, SignedInt):
            imports_scheme.append("SignedInt")
            args.append(("SignedInt(-1)", SignedInt(-1)))
        elif issubclass(arg.type_, UnsignedFloat):
            imports_scheme.append("UnsignedFloat")
            args.append(("UnsignedFloat(0.5)", UnsignedFloat(0.5)))
        elif issubclass(arg.type_, Symbol):
            imports_scheme.append("Symbol")
            args.append(("Symbol('header:title')", Symbol('header:title')))
        elif issubclass(arg.type_, Procedure):
            imports_scheme.append("Procedure")
            args.append((
                "Procedure('(some-procedure)')",
                Procedure('(some-procedure)')))
        elif issubclass(arg.type_, Pair):
            imports_scheme.append("Pair")
            if "SignedInt" not in imports_scheme:
                imports_scheme.append("SignedInt")
            args.append((
                "Pair([SignedInt(0), SignedInt(1)])",
                Pair([SignedInt(0), SignedInt(1)])))
        elif issubclass(arg.type_, AssociationList):
            imports_scheme.append("AssociationList")
            if "SignedInt" not in imports_scheme:
                imports_scheme.append("SignedInt")
            if "Pair" not in imports_scheme:
                imports_scheme.append("Pair")
            args.append((
                "AssociationList([Pair([SignedInt(0), SignedInt(1)])])",
                AssociationList([Pair([SignedInt(0), SignedInt(1)])])))
        elif issubclass(arg.type_, List):
            imports_scheme.append("List")
            if "SignedInt" not in imports_scheme:
                imports_scheme.append("SignedInt")
            args.append((
                "List([SignedInt(0), SignedInt(1), SignedInt(2)])",
                List([SignedInt(0), SignedInt(1), SignedInt(2)])))
        elif issubclass(arg.type_, str):
            args.append(("'test string'", 'test string'))
        else:
            raise InvalidArgument("do not recognize type %r" % arg.type_)
    formatted_parameters = ", ".join(param[0] for param in args)
    content = ""
    content_arg = ""
    if attributes.allowed_content is not None:
        # put something in the content
        # separator between tag/arguments and content
        if len(attributes.arguments) > 0 or attributes.lily_name != "":
            content += " "
        content += "%s " % attributes.delimiter_open
        # figure out what to put inside
        if 'markup' in attributes.allowed_content:
            if 'Italic' not in imports_this:
                imports_this.append("Italic")
            content_arg += "[Italic()]"
            content += r"\italic { }"
        elif 'text' in attributes.allowed_content:
            content_arg = "['test string']"
            content += "test string"
        content += " %s" % attributes.delimiter_close
        if len(formatted_parameters) > 0:
            formatted_parameters += ", %s" % content_arg
        else:
            formatted_parameters = content_arg

    docstring += """
    Examples
    ========
    .. testsetup::

        from lilyflower.dom import {imports}
    """.format(imports=", ".join(imports_this))
    if len(imports_scheme) > 0:
        docstring += """    from lilyflower.schemedata import {imports}
    """.format(imports=", ".join(imports_scheme))

    docstring += """

    .. doctest::

        >>> print format({name}({parameters}))
        {result}
    """.format(
        name=class_name,
        parameters=formatted_parameters,
        result="%s%s%s%s" % (
            attributes.lily_name,
            " " if len(args) > 0 else "",
            " ".join(format(param[1]) for param in args),
            content))
    # TODO: handle position argument

    return docstring
