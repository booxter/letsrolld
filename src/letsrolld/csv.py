import csv


_SKIP_V7 = 4


def lines_to_skip(file_name):
    with open(file_name) as file:
        line = next(file)
    if line.strip() == "Letterboxd list export v7":
        return _SKIP_V7
    return 0


def read_lines(file_name):
    skip = lines_to_skip(file_name)
    with open(file_name) as file:
        while skip > 0:
            next(file)
            skip -= 1
        yield from file


def csv_entries(lines):
    headers = []
    csv_reader = csv.reader(lines)
    for row in csv_reader:
        if not headers:
            headers = row
        else:
            yield dict(zip(headers, row))


def read_csv_file(file_name):
    yield from csv_entries(read_lines(file_name))
