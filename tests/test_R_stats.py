import math
import pytest
from yasss.validation import get_validation_data


@pytest.mark.parametrize(**get_validation_data("power_prop_test"))
def test_power_prop_test(p1, p2, sig_level, power, expected):
    assert math.isclose(p1 + 0.1, p2)
