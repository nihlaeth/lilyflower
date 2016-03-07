"""Some tools."""
import re


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
    None

    Raises
    ======
    :class:`lilyflower.errors.InvalidArgument`:
        if any of the arguments doesn't match the type requirement,
        or if there are too many or too few arguments.
    """
    if attributes.allowed_content is not None:
        docstring += """:class:`lilyflower.errors.InvalidContent`:
        if any of the content does not match the type requirement.
    """

    docstring += """
    Notes
    =====
    """
    # TODO: add some useful notes on parameter resolve order

    # TODO: add see also section

    # TODO: add reference section (maybe a search for command in lily docs?

    return docstring
