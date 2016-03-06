"""
Lilypond syntax definition.

Syntax definition both used in parsing and formatting.
"""
import re
from collections import namedtuple
from UserDict import DictMixin
from lilyflower.schemedata import SignedFloat, String, AssociationList
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

    # pylint: disable=too-many-arguments
    def add(
            self,
            name,
            lily_name,
            types,
            arguments,
            allowed_content,
            inline=False,
            delimiter_open="{",
            delimiter_close="}"):
        """Return named tuple with all the spec info."""
        if re.match("$[a-zA-Z_]+[a-zA-Z0-9_]*^", name) is None:
            raise InvalidArgument("Invalid name %r" % name)
        if re.match("$[a-zA-Z\\\\\\-/_0-9%]*^", lily_name) is None:
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
                raise InvalidArgument("%r is not a dict" % arg)
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
        self._container[name] = SpecItem(
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

# arguments
size = Argument('size', SignedFloat, False)
string = Argument('string', String, False)
assoc_list = Argument('association_list', AssociationList, False)

# markup font functions
SPEC.add('bold', '\\bold', markup_t, None, markup_c)
SPEC.add('italic', '\\italic', markup_t, None, markup_c)
SPEC.add('abs_fontsize', '\\abs-fontsize', markup_t, (size), markup_c)
SPEC.add('box', '\\box', markup_t, None, markup_c)
SPEC.add('caps', '\\caps', markup_t, None, markup_c)
SPEC.add('dynamic_font', '\\dynamic-font', markup_t, None, markup_c)
SPEC.add('finger_font', '\\finger', markup_t, None, markup_c)
SPEC.add('font_caps', '\\fontCaps', markup_t, None, markup_c)
SPEC.add('font_size', '\\font-size', markup_t, (size), markup_c)
SPEC.add('huge', '\\huge', markup_t, None, markup_c)
SPEC.add('large', '\\large', markup_t, None, markup_c)
SPEC.add('larger', '\\larger', markup_t, None, markup_c)
SPEC.add('magnify', '\\magnify', markup_t, (string), markup_c)
SPEC.add('medium', '\\medium', markup_t, None, markup_c)
SPEC.add('normal_size_sub', '\\normal-size-sub', markup_t, None, markup_c)
SPEC.add('normal_size_super', '\\normal-size-super', markup_t, None, markup_c)
SPEC.add('normal_text', '\\normal-text', markup_t, None, markup_c)
SPEC.add('number_font', '\\number', markup_t, None, markup_c)
SPEC.add('replace', '\\replace', markup_t, (assoc_list), markup_c)
SPEC.add('roman_font', '\\roman', markup_t, None, markup_c)
SPEC.add('sans_font', '\\sans', markup_t, None, markup_c)
SPEC.add('simple', '\\simple', markup_t, None, markup_c)
SPEC.add('small', '\\small', markup_t, None, markup_c)
SPEC.add('small_caps', '\\smallCaps', markup_t, None, markup_c)
SPEC.add('smaller', '\\smaller', markup_t, None, markup_c)
SPEC.add('sub', '\\sub', markup_t, None, markup_c)
SPEC.add('super', '\\super', markup_t, None, markup_c)
SPEC.add('teeny', '\\teeny', markup_t, None, markup_c)
SPEC.add('text_font', '\\text', markup_t, None, markup_c)
SPEC.add('tiny', '\\tiny', markup_t, None, markup_c)
SPEC.add('typewriter_font', '\\typewriter', markup_t, None, markup_c)
SPEC.add('underline', '\\underline', markup_t, None, markup_c)
SPEC.add('upright', '\\upright', markup_t, None, markup_c)
