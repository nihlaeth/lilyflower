"""All the lilypond elements."""
from lilyflower.syntax import SPEC
from lilyflower.node import Node
from lilyflower.tools import property_to_class, generate_docstring

for key in SPEC:
    class_name = property_to_class(key)
    attributes = SPEC[key]
    globals()[class_name] = type(
        class_name,
        (Node,),
        {
            '__doc__': generate_docstring(class_name, attributes),
            'tag': attributes.lily_name,
            'types': attributes.types,
            'arguments': attributes.arguments,
            'allowed_content': attributes.allowed_content,
            'inline': attributes.inline,
            'delimiter_open': attributes.delimiter_open,
            'delimiter_close': attributes.delimiter_close})
