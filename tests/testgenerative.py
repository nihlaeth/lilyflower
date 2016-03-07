"""Test the new style Node."""
from lilyflower.dom import *
from lilyflower.schemedata import SignedFloat

markup = Markup([
    Bold([
        Italic([
            AbsFontsize(
                SignedFloat(0),
                [
                    Concat(),
                    Combine(Eyeglasses(), Fermata())]
            )
        ]),
        Bold()
    ])
])
print format(markup)
