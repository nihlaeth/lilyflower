"""Tests for lilyflower.Container."""
from lilyflower import Container
# pylint: disable=no-name-in-module
from nose.tools import assert_equals, assert_list_equal


def test_init():
    """Test Container.__init__()."""
    numbers = [0, 1, 2]
    container = Container(numbers)
    assert_list_equal(container.container, [0, 1, 2])


def test_iter():
    """Test Container iteration."""
    numbers = [0, 1, 2]
    container = Container(numbers)

    for i in enumerate(container):
        assert_equals(i[1], numbers[i[0]])


def test_math():
    """Test Container addition and multiplication."""
    numbers = [0, 1, 2]
    container = Container(numbers)
    container *= 2
    assert_list_equal(container.container, [0, 1, 2, 0, 1, 2])

    container += 5
    assert_list_equal(container.container, [0, 1, 2, 0, 1, 2, 5])

    container += [1, 2]
    assert_list_equal(container.container, [0, 1, 2, 0, 1, 2, 5, 1, 2])


def test_list():
    """Test Container list functionality."""
    numbers = [0, 1, 2]
    container = Container(numbers)
    assert_equals(container[0], 0)
    container[2] = 5
    assert_equals(container[2], 5)
    container.append(4)
    assert_list_equal(container.container, [0, 1, 5, 4])
    container.extend([1])
    assert_equals(container.pop(), 1)
    container.insert(0, 7)
    assert_list_equal(container.container, [7, 0, 1, 5, 4])
    assert_equals(container.count(0), 1)
    assert_equals(container.count(9), 0)
    container.remove(7)
    container.reverse()
    assert_list_equal(container.container, [4, 5, 1, 0])
    container.sort()
    assert_list_equal(container.container, [0, 1, 4, 5])
    del container[1]
    assert_list_equal(container.container, [0, 4, 5])


def test_format():
    """Test Container formatting."""
    container = Container([0, 1, 2])
    result = format(container)
    expected = "\n{\n  0 1 2 \n}\n"
    assert_equals(result, expected)

    # increase indent
    result = format(container, "1")
    expected = "\n  {\n    0 1 2 \n  }\n"
    assert_equals(result, expected)

    # test nesting
    container = Container([0, 1, Container(["test"])])
    result = format(container)
    expected = "\n{\n  0 1 \n  {\n    test \n  }\n\n}\n"
    assert_equals(result, expected)
