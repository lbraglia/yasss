from pathlib import Path
import csv


def get_validation_data(fname):
    """The function is used for procedures validation. It retrieves a csv in
    'validation_data' directory and extract component for
    @pytest.mark.parametrize
    """
    fpath = Path("validation_data") / (fname + ".csv")
    with open(fpath) as csvfile:
        data = list(csv.DictReader(csvfile, quoting=csv.QUOTE_NONNUMERIC))
        vd_header = ", ".join(list(data[0].keys()))
        vd_data = [tuple(row.values()) for row in data]
        vd_ids = [", ".join(tuple(f"{k}={v}"for k, v in row.items()))
                  for row in data]
        return {
            "argnames": vd_header,
            "argvalues": vd_data,
            "ids": vd_ids
        }
