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
            '_tag': attributes.lily_name,
            '_types': attributes.types,
            '_arguments': attributes.arguments,
            '_allowed_content': attributes.allowed_content,
            '_inline': attributes.inline,
            '_delimiter_open': attributes.delimiter_open,
            '_delimiter_close': attributes.delimiter_close})
