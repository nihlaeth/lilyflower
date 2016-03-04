"""Some basic typo catching."""
# pylint: disable=unused-wildcard-import,wildcard-import,invalid-name
from lilyflower.spanners import Slur
from lilyflower.dynamics import Crescendo, Piano, Piano2
from lilyflower.tones import Note, Rest, Chord, Pitch
from lilyflower.commands import Bar
from lilyflower.containers import Staff, Measure, BookPart, LilyFile, Parallel


slur = Slur()
crescendo = Crescendo(Piano())
measure = Measure(
    [
        Note('gis', note_commands=[Piano2(), crescendo], spanners=[slur]),
        Note('as'),
        Note('bes', '', '4.', note_commands=[crescendo], spanners=[slur])],
    [Bar("|.")])

staff = Staff([Note('a', '', '2'), Note('ases'), Note('ais', "'", '4.')])
staff2 = Staff([Rest('4.'), Rest(), Chord([Pitch('a'), Pitch('bes')]), measure])
f = LilyFile([
    BookPart([Parallel([staff, staff2])]),
    BookPart([Bar("||")])])

print format(f)
