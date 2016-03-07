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

## Current state
This project is not even alpha yet - do not use it at this point. I'm still
figuring out what shape this is going to take, so anything is subject to change.

I got diverted into rewriting the lilypond spec and documentation, which is pointless and not what I wanted, so I decided to go a different way.

Command and container classes won't be defined individually, but generated from some syntax rules.

Also, I'm going to try and make use of the work the awesome folks at python-ly did. It currently isn't possible to generate .ly code with their tools, but what they do, they do superbly. No need to invent the wheel twice.

## Installation
```
python setup.py install
```

## Tests
```
python setup.py doctest # requires sphinx
python setup.py test # requires nose
```

If you changed anything in the Node factory chain, make sure to issue
a make clean first (see below), since sphinx does not detect changes in
docstrings of files that haven't been edited.

## Documentation
```
python setup.py html
```
Html documentation will be built in doc/build/html. If the documentation
does not reflect changes in the source, issue a make clean and try again:

```
cd doc && make clean && cd ..
python setup.py html
```

## TODO
- [ ] build in formatting for content lengths > 1
- [ ] add sequence & iterator methods to Node
- [ ] add weakref to Node for object tree traversal
- [ ] add support for objects with an open and close part (spanners, crescendo, etc.)
- [ ] create lilypond data classes (duration, pitch, octave)
- [ ] integrate tone classes into Node
- [ ] add type checking methods to Node (for self.\_type)
- [ ] implement inherited duration & octave (through tree traversal)
- [ ] clean out all the old classes
- [ ] add LilyFile object to dom
- [ ] add support for multi-measure rests
- [ ] add all notecommands (accents and such)
- [ ] have containers check if content is even remotely valid (class checking)
- [x] add all markup commands and containers
- [ ] implement lyrics mode
- [ ] implement chord mode
- [ ] add comments
- [ ] add all music commands and containers
- [x] have containers validate arguments
- [ ] implement lilypond variables & tags (more readable source code)
- [ ] implement property setting
- [ ] better documentation
- [ ] test everything

## Planned features
- [ ] add parser/generators for quick object tree generation
- [ ] expensive & permanent transpose and reverse by having lilypond interpret and parsing result
- [ ] template functions to save time (only write music)
