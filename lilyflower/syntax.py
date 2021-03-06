"""
Lilypond syntax definition.

Syntax definition both used in parsing and formatting.
"""
import re
from collections import namedtuple
from UserDict import DictMixin
from lilyflower.schemedata import (
    SignedFloat,
    String,
    Color,
    List,
    AssociationList,
    Pair,
    Symbol,
    Procedure,
    Boolean,
    SignedInt)
from lilyflower.errors import InvalidArgument

Argument = namedtuple('Argument', 'name type_ optional')
SpecItem = namedtuple('SpecItem', [
    'lily_name',
    'types',
    'arguments',
    'allowed_content',
    'inline',
    'delimiter_open',
    'delimiter_close'])


class Spec(object, DictMixin):

    """Lilypond syntax specification."""

    def __init__(self):
        """Init container."""
        self._container = {}

    def __getattr__(self, attr_name):
        """Each rule is an attribute, if it doesn't exist, create it."""
        if attr_name not in self._container:
            def add_name(*args, **kwargs):
                """Pass the attribute name to add_rule."""
                return self._add_rule(attr_name, *args, **kwargs)
            return add_name
        else:
            return self._container[attr_name]

    # pylint: disable=too-many-arguments
    def _add_rule(
            self,
            rule_name,
            lily_name,
            types,
            arguments,
            allowed_content,
            inline=False,
            delimiter_open="{",
            delimiter_close="}"):
        """Return named tuple with all the spec info."""
        if re.match("^[a-zA-Z_]+[a-zA-Z0-9_]*$", rule_name) is None:
            raise InvalidArgument("Invalid name %r" % rule_name)
        if re.match(r"^[a-zA-Z\\\-/_0-9%]*$", lily_name) is None:
            raise InvalidArgument("Invalid lilypond name %r" % lily_name)

        # this list will likely change in the future
        valid_types = [
            'music',
            'markup',
            'attachment',
            'accent',
            'lyrics',
            'chordmode',
            'comment',
            'setting',
            'field',
            'variable']
        if types is not None and isinstance(types, tuple):
            for item in types:
                if item not in valid_types:
                    raise InvalidArgument("%r not a valid type" % item)
        else:
            raise InvalidArgument("%r not a tuple of types" % types)
        if allowed_content is not None and isinstance(allowed_content, tuple):
            for item in allowed_content:
                if item not in valid_types:
                    raise InvalidArgument("%r not a valid type" % item)
        elif allowed_content is None:
            pass
        else:
            raise InvalidArgument("%r not a tuple of types" % allowed_content)

        if arguments is None:
            arguments = ()
        if not isinstance(arguments, tuple):
            raise InvalidArgument("%r is not a tuple" % arguments)
        for arg in arguments:
            # namedtuple Argument with 3 keys:
            # name
            # type
            # optional
            # Making sure we got what we expected is too expensive,
            # things will crash and burn when user provides the wrong
            # thing here.
            if not isinstance(arg, tuple):
                raise InvalidArgument("%r is not a tuple" % arg)
            if re.match("^[a-zA-Z]+[a-zA-Z0-9_]*$", arg.name) is None:
                raise InvalidArgument("%r is not a valid name" % arg.name)
            # Pretty much anything flies as a type, even if it makes
            # little sense. objects count, instances do not. Strings
            # indicate a spec in this object. Testing is too much
            # hassle, just do something sensible.
            if not isinstance(arg.optional, bool):
                raise InvalidArgument("%r is not a bool" % arg.optional)

        if not isinstance(inline, bool):
            raise InvalidArgument("%r not a boolean value" % inline)
        if not isinstance(delimiter_open, basestring):
            raise InvalidArgument("%r is not a string" % delimiter_open)
        if not isinstance(delimiter_close, basestring):
            raise InvalidArgument("%r is not a string" % delimiter_open)
        self._container[rule_name] = SpecItem(
            lily_name,
            types,
            arguments,
            allowed_content,
            inline,
            delimiter_open,
            delimiter_close)

    def __getitem__(self, key):
        """Get item from container."""
        return self._container[key]

    def __setitem__(self, key, value):
        """Set item in container."""
        # TODO: validate stuff
        self._container[key] = value

    def __delitem__(self, key):
        """Delete item."""
        del self._container[key]

    def keys(self):
        """Return keys."""
        return self._container.keys()

    def __iter__(self):
        """Return iterable."""
        return iter(self._container)

    def __contains__(self, key):
        """Return true if key in container."""
        if key in self._container:
            return True
        else:
            return False


SPEC = Spec()

# Some shortcuts
# pylint: disable = invalid-name

# types _t = type definition, _c = content validation, _= argument type
markup_t = ('markup', 'attachment')
markup_c = ('markup', 'comment', 'setting', 'variable')
markup_a = ('markup', 'variable')
music_c = ('music',)
music_t = ('music', 'comment')
accent_t = ('attachment', 'accent')

# arguments
arg1 = Argument('arg1', markup_a, False)
arg2 = Argument('arg2', markup_a, False)
pattern = Argument('pattern', markup_a, False)
footnote = Argument('footnote', markup_a, False)
gauge = Argument('gauge', markup_a, False)
default = Argument('default', markup_a, False)
string = Argument('string', String, False)
file_name = Argument('file_name', String, False)
url = Argument('url', String, False)
glyph_name = Argument('glyph_name', String, False)
duration = Argument('duration', String, False)
definition_string = Argument('definition_string', String, False)
name = Argument('name', String, False)
filled = Argument('filled', Boolean, False)
axis = Argument('axis', SignedInt, False)
num_strings = Argument('num_strings', SignedInt, False)
num = Argument('num', SignedInt, False)
count = Argument('count', SignedInt, False)
space = Argument('space', SignedFloat, False)
length = Argument('length', SignedFloat, False)
size = Argument('size', SignedFloat, False)
amount = Argument('amount', SignedFloat, False)
direction = Argument('direction', SignedFloat, False)
angle = Argument('angle', SignedFloat, False)
width = Argument('width', SignedFloat, False)
slope = Argument('slope', SignedFloat, False)
radius = Argument('radius', SignedFloat, False)
thickness = Argument('thickness', SignedFloat, False)
blot = Argument('blot', SignedFloat, False)
staff_space = Argument('staff_space', SignedFloat, False)
log = Argument('log', SignedFloat, False)
dot_count = Argument('dot_count', SignedFloat, False)
page_number = Argument('page_number', SignedFloat, False)
symbol = Argument('symbol', Symbol, False)
instrument = Argument('instrument', Symbol, False)
label = Argument('label', Symbol, False)
xext = Argument('xext', Pair, False)
yext = Argument('yext', Pair, False)
factor = Argument('factor', Pair, False)
offset = Argument('offset', Pair, False)
new_property = Argument('new_property', Pair, False)
destination = Argument('destination', Pair, False)
assoc_list = Argument('association_list', AssociationList, False)
commands = Argument('commands', List, False)
markings_list = Argument('markings_list', List, False)
user_draw_commands = Argument('user_draw_commands', List, False)
procedure = Argument('procedure', Procedure, False)
# TODO: create scheme stencil
stencil = Argument('stencil', None, False)
color = Argument('color', Color, False)

# markup container
SPEC.markup(r'\markup', markup_t, None, markup_c)

# markup font
SPEC.abs_fontsize(r'\abs-fontsize', markup_t, (size,), markup_c)
SPEC.bold(r'\bold', markup_t, None, markup_c)
SPEC.box(r'\box', markup_t, None, markup_c)
SPEC.caps(r'\caps', markup_t, None, markup_c)
SPEC.dynamic_font(r'\dynamic-font', markup_t, None, markup_c)
SPEC.finger_font(r'\finger', markup_t, None, markup_c)
SPEC.font_caps(r'\fontCaps', markup_t, None, markup_c)
SPEC.font_size(r'\font-size', markup_t, (size,), markup_c)
SPEC.huge(r'\huge', markup_t, None, markup_c)
SPEC.italic(r'\italic', markup_t, None, markup_c)
SPEC.large(r'\large', markup_t, None, markup_c)
SPEC.larger(r'\larger', markup_t, None, markup_c)
SPEC.magnify(r'\magnify', markup_t, (string,), markup_c)
SPEC.medium(r'\medium', markup_t, None, markup_c)
SPEC.normal_size_sub(r'\normal-size-sub', markup_t, None, markup_c)
SPEC.normal_size_super(r'\normal-size-super', markup_t, None, markup_c)
SPEC.normal_text(r'\normal-text', markup_t, None, markup_c)
SPEC.number_font(r'\number', markup_t, None, markup_c)
SPEC.replace(r'\replace', markup_t, (assoc_list,), markup_c)
SPEC.roman_font(r'\roman', markup_t, None, markup_c)
SPEC.sans_font(r'\sans', markup_t, None, markup_c)
SPEC.simple(r'\simple', markup_t, None, markup_c)
SPEC.small(r'\small', markup_t, None, markup_c)
SPEC.small_caps(r'\smallCaps', markup_t, None, markup_c)
SPEC.smaller(r'\smaller', markup_t, None, markup_c)
SPEC.sub(r'\sub', markup_t, None, markup_c)
SPEC.super(r'\super', markup_t, None, markup_c)
SPEC.teeny(r'\teeny', markup_t, None, markup_c)
SPEC.text_font(r'\text', markup_t, None, markup_c)
SPEC.tiny(r'\tiny', markup_t, None, markup_c)
SPEC.typewriter_font(r'\typewriter', markup_t, None, markup_c)
SPEC.underline(r'\underline', markup_t, None, markup_c)
SPEC.upright(r'\upright', markup_t, None, markup_c)

# markup align
SPEC.center_align(r'\center-align', markup_t, None, markup_c)
SPEC.center_column(r'\center-column', markup_t, None, markup_c)
SPEC.column(r'\column', markup_t, None, markup_c)
SPEC.combine(r'\combine', markup_t, (arg1, arg2), None)
SPEC.concat(r'\concat', markup_t, None, markup_c)
SPEC.dir_column(r'\dir-column', markup_t, None, markup_c)
SPEC.fill_line(r'\fill-line', markup_t, None, None)
SPEC.fill_with_pattern(
    r'\fill-with-pattern',
    markup_t,
    (space, direction, pattern, arg1, arg2),
    None)
SPEC.general_align(
    r'\general-align',
    markup_t,
    (axis, direction),
    markup_c)
SPEC.halign(r'\halign', markup_t, (direction,), markup_c)
SPEC.hcenter_in(r'\hcenter-in', markup_t, (length,), markup_c)
SPEC.hspace(r'\hspace', markup_t, (space,), None)
SPEC.justify_field(r'\justify-field', markup_t, (symbol,), None)
SPEC.justify(r'\justify', markup_t, None, markup_c)
SPEC.justify_string(r'\justify-string', markup_t, (string,), None)
SPEC.left_align(r'\left-align', markup_t, None, markup_c)
SPEC.left_column(r'\left-column', markup_t, None, markup_c)
SPEC.line(r'\line', markup_t, None, markup_c)
SPEC.lower(r'\lower', markup_t, (amount,), markup_c)
SPEC.pad_around(r'\pad-around', markup_t, (amount,), markup_c)
SPEC.pad_markup(r'\pad-markup', markup_t, (amount,), markup_c)
SPEC.pad_to_box(r'\pad-to-box', markup_t, (xext, yext), markup_c)
SPEC.pad_x(r'\pad-x', markup_t, (amount,), markup_c)
SPEC.put_adjacent(
    r'\put-adjacent',
    markup_t,
    (axis, direction, arg1, arg2),
    None)
SPEC.raise_markup(r'\raise', markup_t, (amount,), markup_c)
SPEC.right_align(r'\right-align', markup_t, None, markup_c)
SPEC.right_column(r'\right-column', markup_t, None, markup_c)
SPEC.rotate(r'\rotate', markup_t, (angle,), markup_c)
SPEC.translate(r'\translate', markup_t, (offset,), markup_c)
SPEC.translate_scaled(
    r'\translate-scaled',
    markup_t,
    (offset,),
    markup_c)
SPEC.vcenter(r'\vcenter', markup_t, None, markup_c)
SPEC.vspace(r'\vspace', markup_t, (amount,), None)
SPEC.wordwrap_field(r'\wordwrap-field', markup_t, (symbol,), None)
SPEC.wordwrap(r'\wordwrap', markup_t, None, markup_c)
SPEC.wordwrap_string(r'\wordwrap-string', markup_t, (string,), None)

# markup graphic
SPEC.arrow_head(r'\arrow-head', markup_t, (direction, filled), None)
SPEC.beam(r'\beam', markup_t, (width, slope, thickness), None)
SPEC.bracket(r'\bracket', markup_t, None, markup_c)
SPEC.circle(r'\circle', markup_t, None, markup_c)
SPEC.draw_circle(
    r'\draw-circle',
    markup_t,
    (radius, thickness, filled),
    None)
SPEC.draw_dashed_line(
    r'\draw-dashed-line',
    markup_t,
    (destination,),
    None)
SPEC.draw_dotted_line(
    r'\draw-dotted-line',
    markup_t,
    (destination,),
    None)
SPEC.draw_hline(r'\draw-hline', markup_t, None, None)
SPEC.draw_line(r'\draw-line', markup_t, (destination,), markup_c)
SPEC.ellipse(r'\ellipse', markup_t, None, markup_c)
SPEC.epsfile(r'\epsfile', markup_t, (axis, size, file_name), None)
SPEC.filled_box(r'\filled-box', markup_t, (xext, yext, blot), None)
SPEC.hbracket(r'\hbracket', markup_t, None, markup_c)
SPEC.oval(r'\oval', markup_t, None, markup_c)
SPEC.parenthesize(r'\parenthesize', markup_t, None, markup_c)
SPEC.path(r'\path', markup_t, (thickness, commands), None)
SPEC.postscript(r'\postscript', markup_t, (string,), None)
SPEC.rounded_box(r'\rounded-box', markup_t, None, markup_c)
SPEC.scale(r'\scale', markup_t, (factor,), markup_c)
SPEC.triangle(r'\triangle', markup_t, (filled,), None)
SPEC.with_url(r'\with-url', markup_t, (url,), markup_c)

# markup music
SPEC.custom_tab_clef(
    r'\customTabClef',
    markup_t,
    (num_strings, staff_space),
    None)
SPEC.doubleflat(r'\doubleflat', markup_t, None, None)
SPEC.doublesharp(r'\doublesharp', markup_t, None, None)
# fermata is listed under accents as well as markup
# to make things simpler, we place it under accents only.
# SPEC.fermata(r'\fermata', markup_t, None, None)
SPEC.flat(r'\flat', markup_t, None, None)
SPEC.musicglyph(r'\musicglyph', markup_t, (glyph_name,), None)
SPEC.natural(r'\natural', markup_t, None, None)
SPEC.note_by_number(
    r'\note-by-number',
    markup_t,
    (log, dot_count, direction),
    None)
SPEC.note(r'\note', markup_t, (duration, direction), None)
SPEC.rest_by_number(
    r'\rest-by-number',
    markup_t,
    (log, dot_count),
    None)
SPEC.rest(r'\rest', markup_t, (duration,), None)
SPEC.score(r'\score', markup_t, None, music_c)
SPEC.semiflat(r'\semiflat', markup_t, None, None)
SPEC.semisharp(r'\semisharp', markup_t, None, None)
SPEC.sesquiflat(r'\sesquiflat', markup_t, None, None)
SPEC.sesquisharp(r'\sesquisharp', markup_t, None, None)
SPEC.sharp(r'\sharp', markup_t, None, None)
SPEC.tied_lyric(r'\tied-lyric', markup_t, (string,), None)

# instrument specific markup
SPEC.fret_diagram(r'\fret-diagram', markup_t, (definition_string,), None)
SPEC.fret_diagram_terse(
    r'\fret_diagram_terse',
    markup_t,
    (definition_string,),
    None)
SPEC.fret_diagram_verbose(
    r'\fret-diagram-verbose',
    markup_t,
    (markings_list,),
    None)
SPEC.harp_pedal(r'\harp-pedal', markup_t, (definition_string,), None)
SPEC.woodwind_diagram(
    r'\woodwind-diagram',
    markup_t,
    (instrument, user_draw_commands),
    None)

# according registers markup
SPEC.discant(r'\discant', markup_t, (name,), None)
SPEC.free_bass(r'\freeBass', markup_t, (name,), None)
SPEC.std_bass(r'\stdBass', markup_t, (name,), None)
SPEC.std_bass_iv(r'\stdBassIV', markup_t, (name,), None)
SPEC.std_bass_v(r'\stdBassV', markup_t, (name,), None)
SPEC.std_bass_vi(r'\stdBassVI', markup_t, (name,), None)

# other markup
SPEC.auto_footnote(
    r'\auto-footnote',
    markup_t,
    (arg1, footnote),
    None)
SPEC.backslashed_digit(r'\backslashed-digit', markup_t, (num,), None)
SPEC.char(r'\char', markup_t, (num,), None)
SPEC.eyeglasses(r'\eyeglasses', markup_t, None, None)
SPEC.footnote(r'\footnote', markup_t, (arg1, footnote), None)
SPEC.fraction(r'\fraction', markup_t, (arg1, arg2), None)
SPEC.fromproperty(r'\fromproperty', markup_t, (symbol,), None)
SPEC.leftbrace(r'\leftbrace', markup_t, (size,), None)
SPEC.lookup(r'\lookup', markup_t, (glyph_name,), None)
SPEC.markalphabet(r'\markalphabet', markup_t, (num,), None)
SPEC.markletter(r'\markletter', markup_t, (num,), None)
SPEC.null(r'\null', markup_t, None, None)
SPEC.on_the_fly(r'\on-the-fly', markup_t, (procedure,), markup_c)
SPEC.override(r'\override', markup_t, (new_property,), markup_c)
SPEC.page_link(r'\page-link', markup_t, (page_number,), markup_c)
SPEC.page_ref(
    r'\page-ref',
    markup_t,
    (label, gauge, default),
    None)
SPEC.pattern(
    r'\pattern',
    markup_t,
    (count, axis, space, pattern),
    None)
SPEC.property_recursive(
    r'\property-recursive',
    markup_t,
    (symbol,),
    None)
SPEC.right_brace(r'\right-brace', markup_t, (size,), None)
SPEC.slashed_digit(r'\slashed-digit', markup_t, (num,), None)
SPEC.stencil(r'\stencil', markup_t, (stencil,), None)
SPEC.strut(r'\strut', markup_t, None, None)
SPEC.transparent(r'\transparent', markup_t, None, markup_c)
SPEC.verbatim_file(r'\verbatim-file', markup_t, (name,), None)
SPEC.whiteout(r'\whiteout', markup_t, None, markup_c)
SPEC.with_color(r'\with-color', markup_t, (color,), markup_c)
SPEC.with_dimensions(
    r'\with-dimensions',
    markup_t,
    (xext, yext),
    markup_c)
SPEC.with_link(r'\with-link', markup_t, (label,), markup_c)


# accents
SPEC.accent(r'\accent', accent_t, None, None)
SPEC.espressivo(r'\espressivo', accent_t, None, None)
SPEC.marcato(r'marcato', accent_t, None, None)
SPEC.portato(r'\portato', accent_t, None, None)
SPEC.staccatissimo(r'\staccatissimo', accent_t, None, None)
SPEC.staccato(r'\staccato', accent_t, None, None)
SPEC.tenuto(r'\tenuto', accent_t, None, None)
SPEC.prall(r'\prall', accent_t, None, None)
SPEC.mordent(r'\mordent', accent_t, None, None)
SPEC.prallmordent(r'\prallmordent', accent_t, None, None)
SPEC.turn(r'\turn', accent_t, None, None)
SPEC.upprall(r'\upprall', accent_t, None, None)
SPEC.downprall(r'\downprall', accent_t, None, None)
SPEC.upmordent(r'\upmordent', accent_t, None, None)
SPEC.downmordent(r'\downmordent', accent_t, None, None)
SPEC.lineprall(r'\lineprall', accent_t, None, None)
SPEC.prallprall(r'\prallprall', accent_t, None, None)
SPEC.pralldown(r'\pralldown', accent_t, None, None)
SPEC.prallup(r'\prallup', accent_t, None, None)
SPEC.reverseturn(r'\reverseturn', accent_t, None, None)
SPEC.trill(r'\trill', accent_t, None, None)
SPEC.shortfermata(r'\shortfermata', accent_t, None, None)
SPEC.fermata(r'\fermata', accent_t, None, None)
SPEC.longfermata(r'\longfermata', accent_t, None, None)
SPEC.verylongfermata(r'\verylongfermata', accent_t, None, None)
SPEC.upbow(r'\upbow', accent_t, None, None)
SPEC.downbow(r'\downbow', accent_t, None, None)
SPEC.flageolet(r'\flageolet', accent_t, None, None)
SPEC.snappizzicato(r'\snappizzicato', accent_t, None, None)
SPEC.open(r'\open', accent_t, None, None)
SPEC.halfopen(r'\halfopen', accent_t, None, None)
SPEC.stopped(r'\stopped', accent_t, None, None)
SPEC.lheel(r'\lheel', accent_t, None, None)
SPEC.rheel(r'\rheel', accent_t, None, None)
SPEC.ltoe(r'\ltoe', accent_t, None, None)
SPEC.rtoe(r'\rtoe', accent_t, None, None)
SPEC.segno(r'\segno', accent_t, None, None)
SPEC.coda(r'\coda', accent_t, None, None)
SPEC.vardoda(r'\vardoda', accent_t, None, None)
SPEC.ictus(r'\ictus', accent_t, None, None)
SPEC.accentus(r'\accentus', accent_t, None, None)
SPEC.circulus(r'\circulus', accent_t, None, None)
SPEC.semicirculus(r'\semicirculus', accent_t, None, None)
SPEC.signumcongruentiae(r'\signumcongruentiae', accent_t, None, None)

# music functions
SPEC.absolute(r'\absolute', music_t, None, music_c)
SPEC.acciaccatura(r'\acciaccatura', music_t, None, music_c)
SPEC.accidentalStyle(r'\accidentalStyle', music_t, (style,), None)
SPEC.addChordShape(
    r'\addChordShape',
    music_t,
    (key_symbol, tuning, shape_definition),
    None)
SPEC.addInstrumentDefinition(
    r'\addInstrumentDefinition',
    music_t,
    (name, lst),
    None)
SPEC.addQuote(r'\addQuote', music_t, (name,), music_c)
SPEC.afterGrace(r'\afterGrace', music_t, (main_music, grace),  None)
SPEC.allowPageTurn(r'\allowPageTurn', music_t, None, None)
SPEC.allowVoltaHook(r'\allowVoltaHook', music_t, (bar,), None)
SPEC.alterBroken(r'\alterBroken', music_t, None, music_c)
SPEC.appendToTag(r'\appendToTag', music_t, None, music_c)
SPEC.applyContext(r'\applyContext', music_t, None, music_c)
SPEC.applyMusic(r'\applyMusic', music_t, None, music_c)
SPEC.applyOutput(r'\applyOutput', music_t, None, music_c)
SPEC.appoggiatura(r'\appoggiatura', music_t, None, music_c)
SPEC.assertBeamQuant(r'\assertBeamQuant', music_t, None, music_c)
SPEC.assertBeamSlope(r'\assertBeamSlope', music_t, None, music_c)
SPEC.autochange(r'\autochange', music_t, None, music_c)
SPEC.balloonGrobText(r'\balloonGrobText', music_t, None, music_c)
SPEC.balloonText(r'\balloonText', music_t, None, music_c)
SPEC.bar(r'\bar', music_t, None, music_c)
SPEC.barNumberCheck(r'\barNumberCheck', music_t, None, music_c)
SPEC.bendAfter(r'\bendAfter', music_t, None, music_c)
SPEC.bookOutputName(r'\bookOutputName', music_t, None, music_c)
SPEC.bookOutputSuffix(r'\bookOutputSuffix', music_t, None, music_c)
SPEC.breathe(r'\breathe', music_t, None, music_c)
SPEC.chordRepeats(r'\chordRepeats', music_t, None, music_c)
SPEC.clef(r'\clef', music_t, None, music_c)
SPEC.compoundMeter(r'\compoundMeter', music_t, None, music_c)
SPEC.crossStaff(r'\crossStaff', music_t, None, music_c)
SPEC.cueClef(r'\cueClef', music_t, None, music_c)
SPEC.cueClefUnset(r'\cueClefUnset', music_t, None, music_c)
SPEC.cueDuring(r'\cueDuring', music_t, None, music_c)
SPEC.cueDuringWithClef(r'\cueDuringWithClef', music_t, None, music_c)
SPEC.deadNote(r'\deadNote', music_t, None, music_c)
SPEC.defaultNoteHeads(r'\defaultNoteHeads', music_t, None, music_c)
SPEC.defineBarLine(r'\defineBarLine', music_t, None, music_c)
SPEC.displayLilyMusic(r'\displayLilyMusic', music_t, None, music_c)
SPEC.displayMusic(r'\displayMusic', music_t, None, music_c)
SPEC.displayScheme(r'\displayScheme', music_t, None, music_c)
SPEC.endSpanners(r'\endSpanners', music_t, None, music_c)
SPEC.eventChords(r'\eventChords', music_t, None, music_c)
SPEC.featherDurations(r'\featherDurations', music_t, None, music_c)
SPEC.finger(r'\finger', music_t, None, music_c)
SPEC.footnote(r'\footnote', music_t, None, music_c)
SPEC.grace(r'\grace', music_t, None, music_c)
SPEC.gobdescriptions(r'\gobdescriptions', music_t, None, music_c)
SPEC.harmonicByFret(r'\harmonicByFret', music_t, None, music_c)
SPEC.harmonicByRatio(r'\harmonicByRatio', music_t, None, music_c)
SPEC.harmonicByNote(r'\harmonicByNote', music_t, None, music_c)
SPEC.harmonicsOn(r'\harmonicsOn', music_t, None, music_c)
SPEC.hide(r'\hide', music_t, None, music_c)
SPEC.inStaffSegno(r'\inStaffSegno', music_t, None, music_c)
SPEC.instrumentSwitch(r'\instrumentSwitch', music_t, None, music_c)
SPEC.inversion(r'\inversion', music_t, None, music_c)
SPEC.keepWithTag(r'\keepWithTag', music_t, None, music_c)
SPEC.key(r'\key', music_t, None, music_c)
SPEC.killCues(r'\killCues', music_t, None, music_c)
SPEC.label(r'\label', music_t, None, music_c)
SPEC.language(r'\language', music_t, None, music_c)
SPEC.languageRestore(r'\languageRestore', music_t, None, music_c)
SPEC.languageSaveAndChange(r'\languageSaveAndChange', music_t, None, music_c)
SPEC.makeClusters(r'\makeClusters', music_t, None, music_c)
SPEC.makeDefaultStringTuning(r'\makeDefaultStringTuning', music_t, None, music_c)
SPEC.mark(r'\mark', music_t, None, music_c)
SPEC.modalInversion(r'\modalInversion', music_t, None, music_c)
SPEC.modalTranspose(r'\modalTranspose', music_t, None, music_c)
SPEC.musicMap(r'\musicMap', music_t, None, music_c)
SPEC.noPageBreak(r'\noPageBreak', music_t, None, music_c)
SPEC.noPageTurn(r'\noPageTurn', music_t, None, music_c)
SPEC.octaveCheck(r'\octaveCheck', music_t, None, music_c)
SPEC.offset(r'\offset', music_t, None, music_c)
SPEC.omit(r'\omit', music_t, None, music_c)
SPEC.once(r'\once', music_t, None, music_c)
SPEC.ottava(r'\ottava', music_t, None, music_c)
SPEC.overrideProperty(r'\overrideProperty', music_t, None, music_c)
SPEC.overrideTimeSignature(r'\overrideTimeSignature', music_t, None, music_c)
SPEC.pageBreak(r'\pageBreak', music_t, None, music_c)
SPEC.pageTurn(r'\pageTurn', music_t, None, music_c)
SPEC.palmMute(r'\palmMute', music_t, None, music_c)
SPEC.palmMuteOn(r'\palmMuteOn', music_t, None, music_c)
SPEC.parallelMusic(r'\parallelMusic', music_t, None, music_c)
SPEC.parenthesize(r'\parenthesize', music_t, None, music_c)
SPEC.partcombine(r'\partcombine', music_t, None, music_c)
SPEC.partcombineDown(r'\partcombineDown', music_t, None, music_c)
SPEC.partcombineForce(r'\partcombineForce', music_t, None, music_c)
SPEC.partcombineUp(r'\partcombineUp', music_t, None, music_c)
SPEC.partial(r'\partial', music_t, None, music_c)
SPEC.phrasingSlurDashPattern(r'\phrasingSlurDashPattern', music_t, None, music_c)
SPEC.pitchedTrill(r'\pitchedTrill', music_t, None, music_c)
SPEC.pointAndClickOff(r'\pointAndClickOff', music_t, None, music_c)
SPEC.pointAndClockOn(r'\pointAndClockOn', music_t, None, music_c)
SPEC.pointAndClickTypes(r'\pointAndClickTypes', music_t, None, music_c)
SPEC.pushToTag(r'\pushToTag', music_t, None, music_c)
SPEC.quoteDuring(r'\quoteDuring', music_t, None, music_c)
SPEC.relative(r'\relative', music_t, None, music_c)
SPEC.removeWithTag(r'\removeWithTag', music_t, None, music_c)
SPEC.resetRelativeOctave(r'\resetRelativeOctave', music_t, None, music_c)
SPEC.retrograde(r'\retrograde', music_t, None, music_c)
SPEC.revertTimeSignatureSettings(r'\revertTimeSignatureSettings', music_t, None, music_c)
SPEC.rightHandFinger(r'\rightHandFinger', music_t, None, music_c)
SPEC.scaleDurations(r'\scaleDurations', music_t, None, music_c)
SPEC.settingsFrom(r'\settingsFrom', music_t, None, music_c)
SPEC.shape(r'\shape', music_t, None, music_c)
SPEC.shiftDurations(r'\shiftDurations', music_t, None, music_c)
SPEC.single(r'\single', music_t, None, music_c)
SPEC.skip(r'\skip', music_t, None, music_c)
SPEC.slashedGrace(r'\slashedGrace', music_t, None, music_c)
SPEC.slurDashPattern(r'\slurDashPattern', music_t, None, music_c)
SPEC.spacingTweaks(r'\spacingTweaks', music_t, None, music_c)
SPEC.storePredefinedDiagram(r'\storePredefinedDiagram', music_t, None, music_c)
SPEC.stringTuning(r'\stringTuning', music_t, None, music_c)
SPEC.styledNoteHeads(r'\styledNoteHeads', music_t, None, music_c)
SPEC.tabChordRepeats(r'\tabChordRepeats', music_t, None, music_c)
SPEC.tabChordRepetition(r'\tabChordRepetition', music_t, None, music_c)
SPEC.tag(r'\tag', music_t, None, music_c)
SPEC.temporary(r'\temporary', music_t, None, music_c)
SPEC.tieDashPattern(r'\tieDashPattern', music_t, None, music_c)
SPEC.time(r'\time', music_t, None, music_c)
SPEC.times(r'\times', music_t, None, music_c)
SPEC.tocItem(r'\tocItem', music_t, None, music_c)
SPEC.transpose(r'\transpose', music_t, None, music_c)
SPEC.transposedCueDuring(r'\transposedCueDuring', music_t, None, music_c)
SPEC.transposition(r'\transposition', music_t, None, music_c)
SPEC.tuplet(r'\tuplet', music_t, None, music_c)
SPEC.tupletSpan(r'\tupletSpan', music_t, None, music_c)
SPEC.tweak(r'\tweak', music_t, None, music_c)
SPEC.undo(r'\undo', music_t, None, music_c)
SPEC.unfoldRepeats(r'\unfoldRepeats', music_t, None, music_c)
SPEC.void(r'\void', music_t, None, music_c)
SPEC.withMusicProperty(r'\withMusicProperty', music_t, None, music_c)
SPEC.xNote(r'\xNote', music_t, None, music_c)
SPEC.xNotesOn(r'\xNotesOn', music_t, None, music_c)

