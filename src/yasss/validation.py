import csv
import math
from pathlib import Path


def from_file(fname):
    """Obtain validation data on which setup parametrized validation of
    procedures using pytest.

    The function is used for procedures validation by pytest routine launched
    from project root directory.

    It retrieves a csv in 'validation_data' directory () and extract component
    for @pytest.mark.parametrize. It return a dictionary which can be used as
    such in tests/test_*.py
    - argnames coincide with header of the csv (that is k1, k2, ...) and thus
      the testing function is forced to have as arguments the same name of the
      validation csv.
    - argvalues is set to the raw row of data (v1, v2, ...)
    - test id is set to k1=v1, k2=v2, ... for the row

    Examples
    --------
    >>> ## a dull example
    >>> import math
    >>> import pytest
    >>> from yasss.validation import from_file
    >>>
    >>> @pytest.mark.parametrize(**from_file("power_prop_test"))
    ... def test_power_prop_test(p1, p2, sig_level, power, expected):
    ...    assert math.isclose(p1 + 0.1, p2)
    >>>
    """
    fpath = Path("validation_data") / (fname + ".csv")
    with open(fpath) as csvfile:
        data = list(csv.DictReader(csvfile, quoting=csv.QUOTE_NONNUMERIC))
        argnames = ", ".join(list(data[0].keys()))
        argvalues = [tuple(row.values()) for row in data]
        ids = [", ".join(tuple(f"{k}={v}"for k, v in row.items())) for row in data]
        return {
            "argnames": argnames,
            "argvalues": argvalues,
            "ids": ids
        }


def compare(expected, obtained):
    """Main validation check function."""
    assert math.isclose(expected, obtained)
