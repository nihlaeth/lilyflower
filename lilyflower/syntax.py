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
    Boolean,
    SignedInt)
from lilyflower.errors import InvalidArgument

Argument = namedtuple('Argument', 'name type optional')
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
            # TODO: return instance of node object created with spec
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
        if re.match("^[a-zA-Z\\\\\\-/_0-9%]*$", lily_name) is None:
            raise InvalidArgument("Invalid lilypond name %r" % lily_name)

        # this list will likely change in the future
        valid_types = [
            'music_expression',
            'markup',
            'attachment',
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

# types
markup_t = ('markup', 'attachment')
markup_c = ('markup', 'comment', 'setting', 'variable')
# TODO: define what's allowed in a score
music_c = ('music', 'comment')

# arguments
markup = Argument('markup', markup_c, False)
pattern = Argument('pattern', markup_c, False)
footnote = Argument('footnote', markup_c, False)
gauge = Argument('gauge', markup_c, False)
default = Argument('default', markup_c, False)
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
dot_count = Argument('log', SignedFloat, False)
page_number = Argument('page_number', SignedFloat, False)
# TODO: create scheme symbol (field)
symbol = Argument('symbol', None, False)
instrument = Argument('instrument', None, False)
label = Argument('label', None, False)
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
# TODO: create scheme procedure
procedure = Argument('procedure', None, False)
# TODO: create scheme stencil
stencil = Argument('stencil', None, False)
color = Argument('color', Color, False)

# markup container
SPEC.markup('\\markup', markup_t, None, markup_c)

# markup font
SPEC.abs_fontsize('\\abs-fontsize', markup_t, (size,), markup_c)
SPEC.bold('\\bold', markup_t, None, markup_c)
SPEC.box('\\box', markup_t, None, markup_c)
SPEC.caps('\\caps', markup_t, None, markup_c)
SPEC.dynamic_font('\\dynamic-font', markup_t, None, markup_c)
SPEC.finger_font('\\finger', markup_t, None, markup_c)
SPEC.font_caps('\\fontCaps', markup_t, None, markup_c)
SPEC.font_size('\\font-size', markup_t, (size,), markup_c)
SPEC.huge('\\huge', markup_t, None, markup_c)
SPEC.italic('\\italic', markup_t, None, markup_c)
SPEC.large('\\large', markup_t, None, markup_c)
SPEC.larger('\\larger', markup_t, None, markup_c)
SPEC.magnify('\\magnify', markup_t, (string,), markup_c)
SPEC.medium('\\medium', markup_t, None, markup_c)
SPEC.normal_size_sub('\\normal-size-sub', markup_t, None, markup_c)
SPEC.normal_size_super('\\normal-size-super', markup_t, None, markup_c)
SPEC.normal_text('\\normal-text', markup_t, None, markup_c)
SPEC.number_font('\\number', markup_t, None, markup_c)
SPEC.replace('\\replace', markup_t, (assoc_list,), markup_c)
SPEC.roman_font('\\roman', markup_t, None, markup_c)
SPEC.sans_font('\\sans', markup_t, None, markup_c)
SPEC.simple('\\simple', markup_t, None, markup_c)
SPEC.small('\\small', markup_t, None, markup_c)
SPEC.small_caps('\\smallCaps', markup_t, None, markup_c)
SPEC.smaller('\\smaller', markup_t, None, markup_c)
SPEC.sub('\\sub', markup_t, None, markup_c)
SPEC.super('\\super', markup_t, None, markup_c)
SPEC.teeny('\\teeny', markup_t, None, markup_c)
SPEC.text_font('\\text', markup_t, None, markup_c)
SPEC.tiny('\\tiny', markup_t, None, markup_c)
SPEC.typewriter_font('\\typewriter', markup_t, None, markup_c)
SPEC.underline('\\underline', markup_t, None, markup_c)
SPEC.upright('\\upright', markup_t, None, markup_c)

# markup align
SPEC.center_align('\\center-align', markup_t, None, markup_c)
SPEC.center_column('\\center-column', markup_t, None, markup_c)
SPEC.column('\\column', markup_t, None, markup_c)
SPEC.combine('\\combine', markup_t, (markup, markup), None)
SPEC.concat('\\concat', markup_t, None, markup_c)
SPEC.dir_column('\\dir-column', markup_t, None, markup_c)
SPEC.fill_line('\\fill-line', markup_t, None, None)
SPEC.fill_with_pattern(
    '\\fill-with-pattern',
    markup_t,
    (space, direction, pattern, markup, markup),
    None)
SPEC.general_align(
    '\\general-align',
    markup_t,
    (axis, direction),
    markup_c)
SPEC.halign('\\halign', markup_t, (direction,), markup_c)
SPEC.hcenter_in('\\hcenter-in', markup_t, (length,), markup_c)
SPEC.hspace('\\hspace', markup_t, (space,), None)
SPEC.justify_field('\\justify-field', markup_t, (symbol,), None)
SPEC.justify('\\justify', markup_t, None, markup_c)
SPEC.justify_string('\\justify-string', markup_t, (string,), None)
SPEC.left_align('\\left-align', markup_t, None, markup_c)
SPEC.left_column('\\left-column', markup_t, None, markup_c)
SPEC.line('\\line', markup_t, None, markup_c)
SPEC.lower('\\lower', markup_t, (amount,), markup_c)
SPEC.pad_around('\\pad-around', markup_t, (amount,), markup_c)
SPEC.pad_markup('\\pad-markup', markup_t, (amount,), markup_c)
SPEC.pad_to_box('\\pad-to-box', markup_t, (xext, yext), markup_c)
SPEC.pad_x('\\pad-x', markup_t, (amount,), markup_c)
SPEC.put_adjacent(
    '\\put-adjacent',
    markup_t,
    (axis, direction, markup, markup),
    None)
SPEC.raise_markup('\\raise', markup_t, (amount,), markup_c)
SPEC.right_align('\\right-align', markup_t, None, markup_c)
SPEC.right_column('\\right-column', markup_t, None, markup_c)
SPEC.rotate('\\rotate', markup_t, (angle,), markup_c)
SPEC.translate('\\translate', markup_t, (offset,), markup_c)
SPEC.translate_scaled(
    '\\translate-scaled',
    markup_t,
    (offset,),
    markup_c)
SPEC.vcenter('\\vcenter', markup_t, None, markup_c)
SPEC.vspace('\\vspace', markup_t, (amount,), None)
SPEC.wordwrap_field('\\wordwrap-field', markup_t, (symbol,), None)
SPEC.wordwrap('\\wordwrap', markup_t, None, markup_c)
SPEC.wordwrap_string('\\wordwrap-string', markup_t, (string,), None)

# markup graphic
SPEC.arrow_head('\\arrow-head', markup_t, (direction, filled), None)
SPEC.beam('\\beam', markup_t, (width, slope, thickness), None)
SPEC.bracket('\\bracket', markup_t, None, markup_c)
SPEC.circle('\\circle', markup_t, None, markup_c)
SPEC.draw_circle(
    '\\draw-circle',
    markup_t,
    (radius, thickness, filled),
    None)
SPEC.draw_dashed_line(
    '\\draw-dashed-line',
    markup_t,
    (destination,),
    None)
SPEC.draw_dotted_line(
    '\\draw-dotted-line',
    markup_t,
    (destination,),
    None)
SPEC.draw_hline('\\draw-hline', markup_t, None, None)
SPEC.draw_line('\\draw-line', markup_t, (destination,), markup_c)
SPEC.ellipse('\\ellipse', markup_t, None, markup_c)
SPEC.epsfile('\\epsfile', markup_t, (axis, size, file_name), None)
SPEC.filled_box('\\filled-box', markup_t, (xext, yext, blot), None)
SPEC.hbracket('\\hbracket', markup_t, None, markup_c)
SPEC.oval('\\oval', markup_t, None, markup_c)
SPEC.parenthesize('\\parenthesize', markup_t, None, markup_c)
SPEC.path('\\path', markup_t, (thickness, commands), None)
SPEC.postscript('\\postscript', markup_t, (string,), None)
SPEC.rounded_box('\\rounded-box', markup_t, None, markup_c)
SPEC.scale('\\scale', markup_t, (factor,), markup_c)
SPEC.triangle('\\triangle', markup_t, (filled,), None)
SPEC.with_url('\\with-url', markup_t, (url,), markup_c)

# markup music
SPEC.custom_tab_clef(
    '\\customTabClef',
    markup_t,
    (num_strings, staff_space),
    None)
SPEC.doubleflat('\\doubleflat', markup_t, None, None)
SPEC.doublesharp('\\doublesharp', markup_t, None, None)
SPEC.fermata('\\fermata', markup_t, None, None)
SPEC.flat('\\flat', markup_t, None, None)
SPEC.musicglyph('\\musicglyph', markup_t, (glyph_name,), None)
SPEC.natural('\\natural', markup_t, None, None)
SPEC.note_by_number(
    '\\note-by-number',
    markup_t,
    (log, dot_count, direction),
    None)
SPEC.note('\\note', markup_t, (duration, direction), None)
SPEC.rest_by_number(
    '\\rest-by-number',
    markup_t,
    (log, dot_count),
    None)
SPEC.rest('\\rest', markup_t, (duration,), None)
SPEC.score('\\score', markup_t, None, music_c)
SPEC.semiflat('\\semiflat', markup_t, None, None)
SPEC.semisharp('\\semisharp', markup_t, None, None)
SPEC.sesquiflat('\\sesquiflat', markup_t, None, None)
SPEC.sesquisharp('\\sesquisharp', markup_t, None, None)
SPEC.sharp('\\sharp', markup_t, None, None)
SPEC.tied_lyric('\\tied-lyric', markup_t, (string,), None)

# instrument specific markup
SPEC.fret_diagram('\\fret-diagram', markup_t, (definition_string,), None)
SPEC.fret_diagram_terse(
    '\\fret_diagram_terse',
    markup_t,
    (definition_string,),
    None)
SPEC.fret_diagram_verbose(
    '\\fret-diagram-verbose',
    markup_t,
    (markings_list,),
    None)
SPEC.harp_pedal('\\harp-pedal', markup_t, (definition_string,), None)
SPEC.woodwind_diagram(
    '\\woodwind-diagram',
    markup_t,
    (instrument, user_draw_commands),
    None)

# according registers markup
SPEC.discant('\\discant', markup_t, (name,), None)
SPEC.free_bass('\\freeBass', markup_t, (name,), None)
SPEC.std_bass('\\stdBass', markup_t, (name,), None)
SPEC.std_bass_iv('\\stdBassIV', markup_t, (name,), None)
SPEC.std_bass_v('\\stdBassV', markup_t, (name,), None)
SPEC.std_bass_vi('\\stdBassVI', markup_t, (name,), None)

# other markup
SPEC.auto_footnote(
    '\\auto-footnote',
    markup_t,
    (markup, footnote),
    None)
SPEC.backslashed_digit('\\backslashed-digit', markup_t, (num,), None)
SPEC.char('\\char', markup_t, (num,), None)
SPEC.eyeglasses('\\eyeglasses', markup_t, None, None)
SPEC.footnote('\\footnote', markup_t, (markup, footnote), None)
SPEC.fraction('\\fraction', markup_t, (markup, markup), None)
SPEC.fromproperty('\\fromproperty', markup_t, (symbol,), None)
SPEC.leftbrace('\\leftbrace', markup_t, (size,), None)
SPEC.lookup('\\lookup', markup_t, (glyph_name,), None)
SPEC.markalphabet('\\markalphabet', markup_t, (num,), None)
SPEC.markletter('\\markletter', markup_t, (num,), None)
SPEC.null('\\null', markup_t, None, None)
SPEC.on_the_fly('\\on-the-fly', markup_t, (procedure,), markup_c)
SPEC.override('\\override', markup_t, (new_property,), markup_c)
SPEC.page_link('\\page-link', markup_t, (page_number,), markup_c)
SPEC.page_ref(
    '\\page-ref',
    markup_t,
    (label, gauge, default),
    None)
SPEC.pattern(
    '\\pattern',
    markup_t,
    (count, axis, space, pattern),
    None)
SPEC.property_recursive(
    '\\property-recursive',
    markup_t,
    (symbol,),
    None)
SPEC.right_brace('\\right-brace', markup_t, (size,), None)
SPEC.slashed_digit('\\slashed-digit', markup_t, (num,), None)
SPEC.stencil('\\stencil', markup_t, (stencil,), None)
SPEC.strut('\\strut', markup_t, None, None)
SPEC.transparent('\\transparent', markup_t, None, markup_c)
SPEC.verbatim_file('\\verbatim-file', markup_t, (name,), None)
SPEC.whiteout('\\whiteout', markup_t, None, markup_c)
SPEC.with_color('\\with-color', markup_t, (color,), markup_c)
SPEC.with_dimensions(
    '\\with-dimensions',
    markup_t,
    (xext, yext),
    markup_c)
SPEC.with_link('\\with-link', markup_t, (label,), markup_c)
