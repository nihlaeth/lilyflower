"""All the lilypond elements."""
from lilyflower.syntax import SPEC
from lilyflower.node import Node
from lilyflower.tools import property_to_class, generate_docstring

for key in SPEC:
    class_name = property_to_class(key)
    attributes = SPEC[key]
    # TODO: pass on attributes to class
    globals()[class_name] = type(
        class_name,
        (Node,),
        {'__doc__': generate_docstring(class_name, attributes)})
