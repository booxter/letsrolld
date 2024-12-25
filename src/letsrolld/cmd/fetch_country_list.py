import argparse
import csv
import sys

from sqlalchemy.orm import sessionmaker

from letsrolld import db
from letsrolld.db import models
from letsrolld import lb_list


# TODO: move to common module, reuse everywhere
def is_known_film(film_):
    session = sessionmaker(bind=db.create_engine())()
    film = (
        session.query(models.Film)
        .filter(models.Film.lb_url == film_.url)
        .first()
    )
    if film is not None:
        print(f"Skipping known film: {film_.url}")
        sys.stdout.flush()
        return True
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--country", help="country slug", required=True)
    parser.add_argument(
        "-o", "--output", help="output film list file", required=True
    )
    parser.add_argument(
        "-N", "--new-only", help="whether to filter out movies already present in db", action="store_true"
    )
    args = parser.parse_args()

    # fetch film list
    films = lb_list.MovieCountryList(args.country).films()

    if args.new_only:
        films = (film for film in films if not is_known_film(film))

    # write to file
    with open(args.output, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, dialect=csv.unix_dialect)
        writer.writerow(["Name", "Year", "URL"])

        for film_ in films:
            while True:
                try:
                    writer.writerow([film_.name, film_.year, film_.url])
                    break
                except Exception:
                    print(f"Error writing film: {film_.url}")
                    sys.stdout.flush()
                    continue
            csvfile.flush()
