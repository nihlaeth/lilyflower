# lilyflower
A python interface that sits on top of lilypond.

Goal: programmatically generate music without delving into scheme.

I love lilypond, but I'm not so much in love with scheme. So I decided to
combine the goodness of lilypond with my favorite language: python.

There are a few existing libraries for this, but they did not provide
the functionality that I needed. Extending them seemed unfeasible with
their huge and organically grown codebases. So I decided to mock something
up myself.

To keep everything simple, I do very little syntax checking. I focus
on keeping everything flexible, and trust that the programmer knows
how to write valid lilypond code.

Eventually I'd like to correctly reverse sequences with ties, slurs and
phrasing slurs, make sure that inherited durations are known by the notes
in question, and have notes know if they are being transposed somehow.

For now I'll settle for awesome iterables and easy extensibility.

## Installation
```
python setup.py install
```

## Tests
```
python setup.py doctest # requires sphinx
python setup.py test # requires nose
```

## Documentation
```
python setup.py html
```
Html documentation will be built in doc/build/html. If the documentation
does not reflect changes in the source, issue a make clean and try again:

```
cd doc
make clean
cd ..
python setup.py html
```

## TODO
- [ ] add support for multi-measure rests
- [ ] add all notecommands (accents and such)
- [ ] have containers check if content is even remotely valid (class checking)
- [ ] add all markup commands and containers
- [ ] implement lyrics mode
- [ ] implement chord mode
- [ ] add comments
- [ ] add all music commands and containers
- [ ] have containers validate arguments
- [ ] implement lilypond variables & tags (more readable source code)
- [ ] implement property setting
- [ ] better documentation
- [ ] test everything

## Planned features
- [ ] add parser/generators for quick object tree generation
- [ ] expensive & permanent transpose and reverse by having lilypond interpret and parsing result
- [ ] template functions to save time (only write music)
