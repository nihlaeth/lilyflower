"""Note object - represent a single tone."""


class Note(object):

    """Represent a single tone."""

    def __init__(
            self,
            pitch,
            octave="",
            duration="",
            division=None,
            tie=False,
            attached=None,
            commands=None,
            phrasing=None):
        """
        Initialize note data.

        pitch -> pitch of the note including accidentals (e.g. "es")
        octave -> (string) height of the note - what this means depends
            on context (absolute or relative).
        duration -> (string) tone duration (e.g. "4..")
        division -> (int) used for tremolo
        tie -> (bool) should this note be tied to the next?
        attached -> (list) text attached to note (fingering instructions,
            tempo indications, etc.)
        commands -> (list) commands attached to note (dynamics)
        phrasing -> (list) slurs and phrasing
        """
        self.pitch = pitch
        # TODO: determine if pitch is actually a pitch, or if it's a
        # lilypond string that we need to parse
        self.octave = octave
        self.duration = duration
        self.division = division
        self.tie = tie
        if attached is None:
            self.attached = []
        else:
            self.attached = [] + attached
        if commands is None:
            self.commands = []
        else:
            self.commands = [] + commands
        if phrasing is None:
            self.phrasing = []
        else:
            self.phrasing = [] + phrasing

    def __format__(self):
        """Return note as it should appear in lilypond file."""
        note = "%s%s%s" % (
            self.pitch,
            self.octave,
            self.duration)
        if self.division is not None:
            note += ":%d" % self.division
        if self.tie:
            note += "~"
        note += + "".join([
            "".join(self.attached),
            "".join(self.commands),
            "".join(self.phrasing)])
        return note
