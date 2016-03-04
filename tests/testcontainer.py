"""Tests for lilyflower.Container."""
from lilyflower.container import Container
# pylint: disable=no-name-in-module
from nose.tools import assert_equals, assert_list_equal


# pylint: disable=too-few-public-methods
class Note(object):

    """Mock note."""

    _inline = True

    def __init__(self, note):
        """Set self.note."""
        self.note = note

    def __format__(self, _):
        """Display something."""
        return self.note

    def __eq__(self, other):
        """Compare."""
        if isinstance(other, str):
            if self.note == other:
                return True
        elif isinstance(other, Note):
            if self.note == other.note:
                return True
        return False


def test_init():
    """Test Container.__init__()."""
    notes = [Note('a'), Note('b'), Note('c')]
    container = Container(notes)
    assert_list_equal(
        container._container,
        [Note('a'), Note('b'), Note('c')])


def test_iter():
    """Test Container iteration."""
    notes = [Note('a'), Note('b'), Note('c')]
    container = Container(notes)

    for i in enumerate(container):
        assert_equals(i[1], notes[i[0]])


def test_math():
    """Test Container addition and multiplication."""
    notes = [Note('a'), Note('b'), Note('c')]
    container = Container(notes)
    container *= 2
    assert_list_equal(container._container, ['a', 'b', 'c', 'a', 'b', 'c'])

    container += 'd'
    assert_list_equal(container._container, ['a', 'b', 'c', 'a', 'b', 'c', 'd'])

    container += ['b', 'c']
    assert_list_equal(
        container._container,
        ['a', 'b', 'c', 'a', 'b', 'c', 'd', 'b', 'c'])


def test_list():
    """Test Container list functionality."""
    # pylint: disable = protected-access
    # tests are allowed ;)
    notes = [Note('a'), Note('b'), Note('c')]
    container = Container(notes)
    assert_equals(container[0], 'a')
    container[2] = 'd'
    assert_equals(container[2], 'd')
    container.append('e')
    assert_list_equal(container._container, ['a', 'b', 'd', 'e'])
    container.extend(['c'])
    assert_equals(container.pop(), 'c')
    container.insert(0, 'f')
    assert_list_equal(container._container, ['f', 'a', 'b', 'd', 'e'])
    assert_equals(container.count('a'), 1)
    assert_equals(container.count('g'), 0)
    container.remove('e')
    container.reverse()
    assert_list_equal(container._container, ['d', 'b', 'a', 'f'])
    container.sort()
    assert_list_equal(container._container, ['a', 'b', 'd', 'f'])
    del container[1]
    assert_list_equal(container._container, ['a', 'd', 'f'])


def test_format():
    """Test Container formatting."""
    container = Container([Note('a'), Note('b'), Note('c')])
    result = format(container)
    expected = "{\n  a b c\n}"
    assert_equals(result, expected)

    # increase indent
    result = format(container, "1")
    expected = "{\n    a b c\n  }"
    assert_equals(result, expected)

    # test nesting (single argument = no block)
    container = Container([Note('a'), Note('b'), Container([Note('c')])])
    result = format(container)
    expected = "{\n  a b\n  c\n}"
    assert_equals(result, expected)

    # now check indent when container with content len 1 contains a
    # container
    container = Container([
        Note('a'),
        Note('b'),
        Container([Container([Note('c'), Note('d')])])])
    expected = "{\n  a b\n  {\n    c d\n  }\n}"
    result = format(container)
    assert_equals(result, expected)

    # now check with a container of length != 1
    container = Container([
        Note('a'),
        Note('b'),
        Container([Note('c'), Note('d')])])
    result = format(container)
    expected = "{\n  a b\n  {\n    c d\n  }\n}"
    assert_equals(result, expected)
