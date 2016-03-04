"""Note and rest objects - represent a tonal unit."""
# pylint: disable = too-few-public-methods,relative-import
import re
from errors import (
    InvalidPitch,
    InvalidOctave,
    InvalidDuration,
    InvalidArgument)
from spanners import Spanner
from notecommands import NoteCommand


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

    _inline = True


class NoteCommandMixin(object):

    """Provide methods for dealing with note commands."""

    _note_commands = None

    def _process_note_commands(self, note_commands):
        """Validate and store note commands."""
        if note_commands is None:
            self._note_commands = []
        else:
            self._note_commands = [] + note_commands
        for command in self._note_commands:
            if not isinstance(command, NoteCommand):
                raise InvalidArgument("expected NoteCommand object")

    def _format_note_commands(self):
        """Return lilypond code."""
        if self._note_commands is not None:
            return "".join(format(item) for item in self._note_commands)
        else:
            return ""


class SpannerMixin(object):

    """Provide methods for dealing with spanner objects."""

    _spanners = None

    def _process_spanners(self, spanners):
        """Validate and store spanner objects."""
        if spanners is None:
            self._spanners = []
        else:
            self._spanners = [] + spanners
        for spanner in self._spanners:
            if not isinstance(spanner, Spanner):
                raise InvalidArgument("expected Spanner object")

    def _format_spanners(self):
        """Return lilypond code."""
        if self._note_commands is not None:
            return "".join(format(item) for item in self._spanners)
        else:
            return ""


class Pitch(Tone):

    """Pitch - octave and pitch without duration."""

    def __init__(self, pitch, octave=""):
        """Set basic data."""
        self._pitch = pitch
        _validate_pitch(pitch)
        self.octave = octave
        _validate_octave(octave)

    def __format__(self, _):
        """Pitch in lilypond format."""
        return "%s%s" % (self._pitch, self.octave)


class Rest(Tone, NoteCommandMixin):

    """Rest - duration - no octave and pitch."""

    def __init__(self, duration="", note_commands=None):
        """Set basic data."""
        self._duration = duration
        _validate_duration(duration)
        self._process_note_commands(note_commands)

    def __format__(self, _):
        """Return lilypond code."""
        return "r%s%s" % (self._duration, self._format_note_commands())


class Note(Tone, NoteCommandMixin, SpannerMixin):

    """Represent a single pitch."""

    def __init__(
            self,
            pitch,
            octave="",
            duration="",
            division=None,
            tie=False,
            note_commands=None,
            spanners=None):
        """
        Initialize note data.

        pitch -> pitch of the note including accidentals (e.g. "es")
        octave -> (string) height of the note - what this means depends
            on context (absolute or relative).
        duration -> (string) pitch duration (e.g. "4..")
        division -> (int) used for tremolo
        tie -> (bool) should this note be tied to the next?
        note_commands -> (list) text and comnands attached to
            note (fingering instructions, dynamics, tempo indications, etc.)
        spanners -> (list) slurs and phrasing
        """
        self._pitch = pitch
        _validate_pitch(pitch)
        self.octave = octave
        _validate_octave(octave)
        self._duration = duration
        _validate_duration(duration)
        self._division = division
        # TODO: validate division
        self._tie = tie
        self._process_note_commands(note_commands)
        self._process_spanners(spanners)

    def __format__(self, _):
        """Return note as it should appear in lilypond file."""
        note = "%s%s%s" % (
            self._pitch,
            self.octave,
            self._duration)
        if self._division is not None:
            note += ":%d" % self._division
        if self._tie:
            note += "~"
        note += "".join([
            self._format_note_commands(),
            self._format_spanners()])
        return note


class Chord(Tone, NoteCommandMixin, SpannerMixin):

    """All the goodness of notes, but with more of them together."""

    def __init__(
            self,
            pitches,
            duration="",
            division=None,
            tie=False,
            note_commands=None,
            spanners=None):
        """
        Set basic data.

        pitches -> (list of Pitch objects) pitches that make up the chord
        duration -> (str) duration of entire chord
        division -> (int) used for tremolo
        tie -> (bool) if the entire chord should be tied to the next note
        note_commands -> (list) related note_commands and text
        spanners -> (list) slur- and phrasing marks
        """
        # TODO: pitches inside a chord can be tied - allow this
        # TODO: implement chord mode
        self._pitches = pitches
        for pitch in pitches:
            if not isinstance(pitch, Pitch):
                raise InvalidArgument("expected a pitch object: %s" % pitch)
        self._duration = duration
        _validate_duration(duration)
        self._division = division
        # TODO: validate division
        self._tie = tie
        self._process_note_commands(note_commands)
        self._process_spanners(spanners)

    def __format__(self, _):
        """Return note as it should appear in lilypond file."""
        note = "< %s>%s" % (
            " ".join(format(pitch) for pitch in self._pitches),
            self._duration)
        if self._division is not None:
            note += ":%d" % self._division
        if self._tie:
            note += "~"
        note += "".join([
            self._format_note_commands(),
            self._format_spanners()])
        return note
