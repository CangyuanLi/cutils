import pytest

from cutils import cutils


def test_contains():
    assert cutils.contains("a", "bce") is False
    assert cutils.contains("a", "alde") is True
    assert cutils.contains([2, 3, 4], [3, 4]) is True
    assert cutils.contains(list(range(0, 100000)), {9, 100}) is True
    assert cutils.contains({9, 100}, list(range(0, 100000))) is True
    assert cutils.contains("abcdefg", "hijk") is False
    assert cutils.contains("abcdefg", "a") is True


def test_chunk_seq():
    test_list = [1, 2, 3, 4, 5, 6, 7]
    assert cutils.chunk_seq(test_list, 2) == [[1, 2], [3, 4], [5, 6], [7]]
    assert cutils.chunk_seq([], 2) == []
    assert cutils.chunk_seq("abcdefgh", 4) == ["abcd", "efgh"]


def test_clamp():
    assert cutils.clamp(5, 1, 2) == 2
    assert cutils.clamp(0, 1, 2) == 1


def test_random_chunk_seq():
    test_list = [1, 2, 3, 4, 5, 6, 7, 9, 10]
    assert cutils.flatten(cutils.random_chunk_seq(test_list, 2, 5)) == test_list


def test_even_split():
    test_list = [1, 2, 3, 4, 5]
    assert cutils.even_split(test_list, 6) == [[1], [2], [3], [4], [5], []]
    assert cutils.even_split((1, 2, 3), 3) == [(1,), (2,), (3,)]


def test_find_last_index():
    test_list = [4, 2, 4, 4, 2]
    assert cutils.find_last_index(test_list, 2) == 4

    with pytest.raises(ValueError):
        cutils.find_last_index(test_list, 3)


def test_flatten():
    test_list = [[1], [2], "ab", 3]
    assert cutils.flatten(test_list) == [1, 2, "ab", 3]

    test_list = [[[[[[[1]]]]]]]
    assert cutils.flatten(test_list) == [1]


def test_flatten_dict():
    pass


def test_get_factors():
    assert cutils.get_factors(10) == {2, 5, 1, 10}

    with pytest.raises(ValueError):
        cutils.get_factors(1.1)


def test_ordered_unique():
    assert cutils.ordered_unique("abbcb") == ["a", "b", "c"]


def test_strip_blanks():
    assert cutils.strip_blanks("a   bc\u2009") == "abc"
    assert cutils.strip_blanks("a") == "a"
