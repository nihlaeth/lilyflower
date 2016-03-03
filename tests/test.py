"""Some basic typo catching."""
# pylint: disable=unused-wildcard-import,wildcard-import,invalid-name
from lilyflower import *

# c = Container([1, 2, 3, Container(["test", Container(["test2"])])])
# print format(c, "1")

slur = Slur()
measure = Measure(
    [
        Note('gis', phrasing=[slur]),
        Note('as'),
        Note('bes', '', '4.', phrasing=[slur])],
    [Bar("|.")])

staff = Staff([Note('a', '', '2'), Note('ases'), Note('ais', "'", '4.')])
staff2 = Staff([Rest('4.'), Rest(), Chord([Pitch('a'), Pitch('bes')]), measure])
f = LilyFile([
    BookPart([Parallel([staff, staff2])]),
    BookPart([Bar("||")])])

print format(f)
