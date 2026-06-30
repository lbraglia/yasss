from pathlib import Path
import csv


def get_validation_data(fname):
    fpath = Path("validation_data") / (fname + ".csv")
    with open(fpath) as csvfile:
        data = list(csv.DictReader(csvfile, quoting=csv.QUOTE_NONNUMERIC))
        vd_name = ", ".join(list(data[0].keys()))
        vd_data = [(tuple(row.values())) for row in data]
        return vd_name, vd_data
        # breakpoint()
        # # vd_data = [(v) for]
        # # return vd_name, vd_data
        # r.values() for row in data
