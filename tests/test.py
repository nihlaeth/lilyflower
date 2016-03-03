"""Some basic typo catching."""
# pylint: disable=unused-wildcard-import,wildcard-import,invalid-name
from lilyflower import *


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
