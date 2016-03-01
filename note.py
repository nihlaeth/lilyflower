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
            attached=[],
            commands=[],
            phrasing=[]):
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
        self.octave = octave
        self.duration = duration
        self.division = division
        self.tie = tie
        self.attached = [] + attached
        self.commands = [] + commands
        self.phrasing = [] + phrasing

    def get_duration(self, context=None):
        """
        Return duration of note.

        Duration can be set directly, or inherited implicitly.
        If duration is not set directly, Note needs the iterable
        that it is itself a part of to determine note duration.
        """
        if self.duration != "":
            return self.duration
        elif context is None:
            # TODO: raise error - no duration and no context
            pass
        try:
            i = context.index(self)
        except ValueError:
            # TODO: raise error - self not found in context
            pass
        if i == 0:
            # TODO: raise error - no previous notes to inherit from
            pass
        return context[i-1].get_duration(context)

    def __repr__(self):
        """Print note as it should appear in lilypond file."""
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
