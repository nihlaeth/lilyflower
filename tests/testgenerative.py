"""Test the new style Node."""
from lilyflower.dom import *
from lilyflower.schemedata import SignedFloat

markup = LilyFile([Markup([
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
])])
print format(markup)

print "\nIterating in-depth"
for item in markup.iter_depth():
    print "\nNext iteration"
    print format(item)
