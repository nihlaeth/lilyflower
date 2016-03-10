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

## Design decisions
### Whitespace
Situation: len(Node.\_content) == 1

Old:
```
\tag \content {
  \content-of-content
  \more-content
}
```
Ups and downs: special cases need to be defined - some tags always need braces. Takes up a lot of vertical space with non-container content.

New:
```
\tag { \content {
  \content-of-content
  \more-content
} }
```
Ups and downs: ugly, slightly confusing.

Alternative:
```
\tag {
  \content {
    \content-of-content
    \more-content
  }
}
```
Ups and downs: clear, beautiful, larger indents leaving less space for music on a signle rule. Takes up a lot more vertical space with non-container content.

Right now, new is implemented. We might decide to switch to Alternative before all's said and done.

### Tone inheritance
In lilypond, tones inherit length and octave from their predecessors. Implementing this would be complex. It would be very useful to the end-user on the other side. This would also be useful for correct reversal with tempo and key changes.

For now other tasks have higher priority.

### Spanners
Spanners are complex because they break the rigid nesting structure. I've chosen to implement the opening and closing part of a spanner as the same object, and to display them according to the number of times format has been called on them.

Another Node that could make use of this is the Variable. First time around it displays its definition, every time after it just displays the tag.

Upside is that spanners are always displayed correctly even after a reversal. It's also relatively simple to validate a node tree by checking if every spanner occurs twice.

Downside is that this breaks if the end-user decides to format part of the node tree that contains one of the references, but not the other. Maybe implement a reset call for the final format?

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
- [ ] add math to Node
- [ ] add weakref to Node for object tree traversal
- [ ] add support for objects with an open and close part (spanners, crescendo, etc.)
- [ ] create lilypond data classes (duration, pitch, octave)
- [ ] integrate tone classes into Node
- [ ] implement inherited duration & octave (through tree traversal)
- [ ] clean out all the old classes
- [ ] add support for multi-measure rests
- [ ] add all notecommands (accents and such)
- [ ] implement lyrics mode
- [ ] implement chord mode
- [x] add comments
- [ ] add all music commands and containers
- [ ] implement lilypond variables & tags (more readable source code)
- [ ] implement property setting
- [ ] better documentation
- [ ] test everything

## Planned features
- [ ] add parser/generators for quick object tree generation
- [ ] expensive & permanent transpose and reverse by having lilypond interpret and parsing result
- [ ] template functions to save time (only write music)
