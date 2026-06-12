import pytest

from librandomizer import LibRandom, randomChar, randomFloat, randomInt, random_char, random_float, random_int


def test_random_int_returns_value_in_inclusive_range():
    value = LibRandom().random_int(min=10, max=20)

    assert 10 <= value <= 20
    assert isinstance(value, int)


def test_random_int_allows_equal_boundaries():
    assert LibRandom().random_int(min=7, max=7) == 7


def test_random_int_rejects_invalid_range():
    with pytest.raises(ValueError, match="min must be less than or equal to max"):
        LibRandom().random_int(min=2, max=1)


def test_random_float_returns_value_in_range():
    value = LibRandom().random_float(min=1.5, max=2.5)

    assert 1.5 <= value <= 2.5
    assert isinstance(value, float)


def test_random_float_allows_equal_boundaries():
    assert LibRandom().random_float(min=3.25, max=3.25) == 3.25


def test_random_float_rejects_invalid_range():
    with pytest.raises(ValueError, match="min must be less than or equal to max"):
        LibRandom().random_float(min=2.0, max=1.0)


def test_random_char_returns_value_in_inclusive_range():
    value = LibRandom().random_char(min="A", max="C")

    assert "A" <= value <= "C"
    assert len(value) == 1


def test_random_char_allows_equal_boundaries():
    assert LibRandom().random_char(min="X", max="X") == "X"


def test_random_char_rejects_invalid_range():
    with pytest.raises(ValueError, match="min must be less than or equal to max"):
        LibRandom().random_char(min="Z", max="A")


@pytest.mark.parametrize("bad_value", ["", "AB", "\n"])
def test_random_char_rejects_invalid_characters(bad_value):
    with pytest.raises(ValueError, match="Invalid character range"):
        LibRandom().random_char(min=bad_value, max="Z")


def test_legacy_import_shim_and_method_aliases_work():
    from libRandom import LibRandom as LegacyLibRandom

    generator = LegacyLibRandom()

    assert generator.get_random_int(1, 1) == 1
    assert generator.get_random_float(1.0, 1.0) == 1.0
    assert generator.get_random_char(65, 65) == "A"


def test_function_first_api_works_with_idiomatic_and_camel_case_names():
    assert random_int(min=4, max=4) == 4
    assert random_float(min=4.5, max=4.5) == 4.5
    assert random_char(min="M", max="M") == "M"
    assert randomInt(5, 5) == 5
    assert randomFloat(5.5, 5.5) == 5.5
    assert randomChar("N", "N") == "N"
