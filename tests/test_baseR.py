import pytest
import math
from yasss.validation import get_validation_data

# obtain the csv structure and its data
vd_head, vd_data = get_validation_data("power_prop_test")
# run the following function for each row of the
@pytest.mark.parametrize(vd_head, vd_data)
#run the following function for each row of the csv
def test_power_prop_test(p1, p2, sig_level, power, expected):
    assert math.isclose(p1 + 0.1, p2)
