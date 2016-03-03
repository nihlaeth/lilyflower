"""Note and rest objects - represent a tonal unit."""
# pylint: disable = too-few-public-methods,relative-import
import re
from errors import InvalidPitch, InvalidOctave, InvalidDuration, InvalidArgument


def _validate_pitch(pitch):
    """Validate pitch."""
    # first character has to be in abcdefg
    # followed by (es|s|is)(es|is)* for accidentals
    # the 's' is for the es, and as (dutch pronounciation doesn't allow
    # for ees or aes).
    regex = "^[a-g]([!?]|(s)?(es|is|eh|ih)*)$"
    if re.match(regex, pitch) is None:
        raise InvalidPitch("%s is not a valid pitch" % pitch)


def _validate_octave(octave):
    """Validate octave."""
    regex = "^(=)?[',]*$"
    if re.match(regex, octave) is None:
        raise InvalidOctave("%s is not a valid octave" % octave)


def _validate_duration(duration):
    """Validate duration."""
    # actually, rests can only be powers of two, but we don't check for that
    regex = "^([0-9]+[.]*|[0-9]*)$"
    if re.match(regex, duration) is None:
        raise InvalidDuration("%s is not a valid duration" % duration)


class Tone(object):

    """Grouping class so tones can be recognized."""

    inline = True


class Pitch(Tone):

    """Pitch - octave and pitch without duration."""

    def __init__(self, pitch, octave=""):
        """Set basic data."""
        self.pitch = pitch
        _validate_pitch(pitch)
        self.octave = octave
        _validate_octave(octave)

    def __format__(self, _):
        """Pitch in lilypond format."""
        return "%s%s" % (self.pitch, self.octave)


class Rest(Tone):

    """Rest - duration - no octave and pitch."""

    def __init__(self, duration=""):
        """Set basic data."""
        self.duration = duration
        _validate_duration(duration)

    def __format__(self, _):
        """Rests in lilypond format."""
        return "r%s" % self.duration


class Note(Tone):

    """Represent a single pitch."""

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
        duration -> (string) pitch duration (e.g. "4..")
        division -> (int) used for tremolo
        tie -> (bool) should this note be tied to the next?
        attached -> (list) text attached to note (fingering instructions,
            tempo indications, etc.)
        commands -> (list) commands attached to note (dynamics)
        phrasing -> (list) slurs and phrasing
        """
        self.pitch = pitch
        _validate_pitch(pitch)
        self.octave = octave
        _validate_octave(octave)
        self.duration = duration
        _validate_duration(duration)
        self.division = division
        # TODO: validate division
        self.tie = tie
        if attached is None:
            self.attached = []
        else:
            self.attached = [] + attached
            # TODO: validate contents of attached
        if commands is None:
            self.commands = []
        else:
            self.commands = [] + commands
            # TODO: validate contents of commands
        if phrasing is None:
            self.phrasing = []
        else:
            self.phrasing = [] + phrasing
            # TODO: validate contents of phrasing

    def __format__(self, _):
        """Return note as it should appear in lilypond file."""
        note = "%s%s%s" % (
            self.pitch,
            self.octave,
            self.duration)
        if self.division is not None:
            note += ":%d" % self.division
        if self.tie:
            note += "~"
        note += "".join([
            "".join(self.attached),
            "".join(self.commands),
            "".join(format(item) for item in self.phrasing)])
        return note


class Chord(Tone):

    """All the goodness of notes, but with more of them together."""

    def __init__(
            self,
            pitches,
            duration="",
            division=None,
            tie=False,
            attached=None,
            commands=None,
            phrasing=None):
        """
        Set basic data.
        
        pitches -> (list of Pitch objects) pitches that make up the chord
        duration -> (str) duration of entire chord
        division -> (int) used for tremolo
        tie -> (bool) if the entire chord should be tied to the next note
        attached -> (list) attached text
        commands -> (list) related commands
        phrasing -> (list) slur- and phrasing marks
        """
        # TODO: pitches inside a chord can be tied - allow this
        # TODO: implement chord mode
        self.pitches = pitches
        for pitch in pitches:
            if not isinstance(pitch, Pitch):
                raise InvalidArgument("expected a pitch object: %s" % pitch)
        self.duration = duration
        _validate_duration(duration)
        self.division = division
        # TODO: validate division
        self.tie = tie
        if attached is None:
            self.attached = []
        else:
            self.attached = [] + attached
            # TODO: validate
        if commands is None:
            self.commands = []
        else:
            self.commands = [] + commands
            # TODO: validate
        if phrasing is None:
            self.phrasing = []
        else:
            self.phrasing = [] + phrasing
            # TODO: validate

    def __format__(self, _):
        """Return note as it should appear in lilypond file."""
        note = "< %s>%s" % (
            " ".join(format(pitch) for pitch in self.pitches),
            self.duration)
        if self.division is not None:
            note += ":%d" % self.division
        if self.tie:
            note += "~"
        note += "".join([
            "".join(self.attached),
            "".join(self.commands),
            "".join(format(item) for item in self.phrasing)])
        return note


