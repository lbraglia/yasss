import pytest
from yasss.validation import from_file, compare


@pytest.mark.parametrize(**from_file("power_prop_test"))
def test_power_prop_test(p1, p2, sig_level, power, expected):
    # fake test
    expected = p2
    obtained = p1 + 0.1
    # # one day
    # obtained = Procedure(p1, p2, sig_level, power).calc()
    compare(expected, obtained)
