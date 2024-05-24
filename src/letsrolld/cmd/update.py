import argparse
import datetime
import math
import sys
import time

import traceback

from sqlalchemy import func, select, or_
from sqlalchemy.orm import sessionmaker

from letsrolld import db
from letsrolld.db import models
from letsrolld import director as dir_obj
from letsrolld import film as film_obj
from letsrolld import http


_MAX_RATING = 5
_SEC_WAIT_ON_FAIL = 5
_LAST_CHECKED_FIELD = "last_checked"
_LAST_UPDATED_FIELD = "last_updated"


_NOW = datetime.datetime.now()

_MIN_REFRESH_FREQUENCY = datetime.timedelta(days=180)


MODEL_TO_THRESHOLD = {
    models.Film: datetime.timedelta(days=7),
    models.Director: datetime.timedelta(days=1),
}


def _get_obj_to_update_query(model, threshold, last_checked_field):
    field = getattr(model, last_checked_field)
    return or_(
        field < _NOW - threshold,
        field > _NOW,
        field == None,  # noqa
    )


def _seen_obj_query(model, seen):
    return model.id.notin_(seen)


def get_obj_to_update(session, model, threshold, last_checked_field, seen):
    return (
        session.execute(
            select(model)
            .filter(_get_obj_to_update_query(model, threshold, last_checked_field))
            .filter(_seen_obj_query(model, seen))
            .limit(1)
        )
        .scalars()
        .first()
    )


def get_number_of_objs_to_update(session, model, threshold, last_checked_field):
    try:
        return session.scalar(
            select(func.count())
            .select_from(model)
            .filter(_get_obj_to_update_query(model, threshold, last_checked_field))
        )
    finally:
        session.close()


def get_objs(session, model, names):
    objs = []
    for name in names:
        db_obj = session.query(model).filter_by(name=name).first()
        objs.append(db_obj)
    return objs


def get_genres(session, genres):
    return get_objs(session, models.Genre, genres)


def get_countries(session, countries):
    return get_objs(session, models.Country, countries)


def get_offers(session, offers):
    return get_objs(session, models.Offer, offers)


def update_objs(session, model, names):
    objs = []
    for name in names:
        db_obj = session.query(model).filter_by(name=name).first()
        if db_obj is not None:
            objs.append(db_obj)
            continue
        db_obj = model(name=name)
        session.add(db_obj)
        objs.append(db_obj)
        print(f"Adding {model.__name__.lower()}: {name}")
    return objs


def update_genres(session, genres):
    return update_objs(session, models.Genre, genres)


def update_countries(session, countries):
    return update_objs(session, models.Country, countries)


def update_offers(session, offers):
    return update_objs(session, models.Offer, {o.technical_name for o in offers})


def add_films(session, films):
    for f in films:
        print(f"Adding film: {f.name} @ {f.url}")
        session.add(
            models.Film(
                title=f.name,
                description=f.description,
                year=f.year,
                rating=f.rating,
                runtime=f.runtime,
                lb_url=f.url,
                jw_url=f.jw_url,
            )
        )


def get_db_film(session, url):
    return session.query(models.Film).filter_by(lb_url=url).first()


def get_db_films(session, films):
    for f in films:
        yield get_db_film(session, f.url)


def touch_obj(session, obj, last_checked_field, last_updated_field, updated=False):
    if updated:
        setattr(obj, last_updated_field, _NOW)
    # cap the last_updated field to the current time
    setattr(obj, last_updated_field, min(_NOW, obj.last_updated or _NOW))
    setattr(obj, last_checked_field, _NOW)
    session.add(obj)


def year(f):
    return f.year or 0


def director_threshold(d):
    multiplier = 1
    if d is None:
        return multiplier

    films = sorted(d.films, key=lambda f: year(f), reverse=True)

    current_year = _NOW.year
    for f in films[:2]:
        multiplier *= max(1, current_year - year(f))
        current_year = year(f)

    return multiplier


def film_threshold(f):
    multiplier = 1
    if f is None:
        return multiplier

    multiplier = max(0, _NOW.year - year(f)) + 1
    return min(100, multiplier)


def offer_threshold(f):
    multiplier = 1
    if f is None:
        return multiplier
    # refresh offers for newer films more often
    multiplier = max(0, _NOW.year - year(f)) + 1
    # cap the multiplier at 14 (weeks)
    return min(14, multiplier)


def skip_obj(obj, last_updated_field, threshold_func, threshold):
    last_updated = getattr(obj, last_updated_field)
    if last_updated:
        return _NOW - min(_NOW, last_updated) <= min(
            _MIN_REFRESH_FREQUENCY, threshold * threshold_func(obj)
        )
    return False


def refresh_director(session, db_obj, api_obj):
    films = list(api_obj.films())

    # don't refresh existing films here
    new_films = [f for f in films if not get_db_film(session, f.url)]
    add_films(session, new_films)
    db_obj.films = list(get_db_films(session, films))


def report_offer_changes(session, db_obj, api_obj):
    old_names = set(
        o.name
        for o in session.query(models.Offer)
        .join(models.FilmOffer)
        .filter(models.FilmOffer.film_id == db_obj.id)
        .all()
    )
    new_names = set(o.technical_name for o in api_obj.available_services)
    old = old_names - new_names
    new = new_names - old_names
    if new or old:
        for o in new:
            print(f"\t+ {o}")
        for o in old:
            print(f"\t- {o}")


def refresh_film(session, db_obj, api_obj):
    # just in case genres or countries or offers changed
    update_genres(session, api_obj.genres)
    update_countries(session, api_obj.countries)

    if not math.isclose(float(api_obj.rating), db_obj.rating):
        print(f"\t{db_obj.rating:.3f} -> {api_obj.rating}")

    db_obj.title = api_obj.name
    db_obj.description = api_obj.description
    db_obj.year = api_obj.year
    db_obj.rating = api_obj.rating
    db_obj.runtime = api_obj.runtime
    db_obj.jw_url = api_obj.jw_url
    db_obj.trailer_url = api_obj.trailer_url
    db_obj.genres = get_genres(session, api_obj.genres)
    db_obj.countries = get_countries(session, api_obj.countries)
    db_obj.last_updated = _NOW


def refresh_offers(session, db_obj, api_obj):
    # just in case genres or countries or offers changed
    db_offers = update_offers(session, api_obj.available_services)

    def get_offer_id(offer):
        return next(o.id for o in db_offers if o.name == offer)

    report_offer_changes(session, db_obj, api_obj)
    for offer in api_obj.available_services:
        obj = (
            session.query(models.FilmOffer)
            .filter_by(film_id=db_obj.id, offer_id=get_offer_id(offer.technical_name))
            .first()
        )
        if  obj is not None:
            obj.url = offer.url
        else:
            obj = models.FilmOffer(
                film_id=db_obj.id,
                offer_id=get_offer_id(offer.technical_name),
                url=offer.url,
            )
            session.add(obj)
    db_obj.last_offers_updated = _NOW


def run_update(
    session,
    model,
    api_cls,
    refresh_func,
    threshold_func,
    threshold,
    last_checked_field,
    last_updated_field,
    dry_run=False,
):
    model_name = model.__name__

    n_objs = get_number_of_objs_to_update(session, model, threshold, last_checked_field)

    i = 1
    seen = set()

    def maybe_commit():
        if dry_run:
            session.rollback()
        else:
            session.commit()

    def loop_housekeeping(session, obj, updated=False):
        touch_obj(
            session,
            obj,
            last_checked_field,
            last_updated_field,
            updated=updated,
        )
        if dry_run:
            # build the list of seen objects only when we cannot rely on
            # last_checked fields in db
            seen.add(obj.id)
        maybe_commit()
        sys.stdout.flush()
        nonlocal i
        i += 1

    while True:
        obj = get_obj_to_update(session, model, threshold, last_checked_field, seen)
        if obj is None:
            break

        if skip_obj(obj, last_updated_field, threshold_func, threshold):
            loop_housekeeping(session, obj, updated=False)
            continue

        print(
            f"{i}/{n_objs}: Updating {model_name}: {obj.name} @ {obj.lb_url}",
            flush=True,
        )

        api_obj = api_cls(obj.lb_url)
        refresh_func(session, obj, api_obj)

        loop_housekeeping(session, obj, updated=True)

    # TODO: is there a better way to extract plural names?
    print(f"No more {model_name}s to update")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main(
    model,
    api_cls,
    refresh_func,
    threshold_func,
    last_checked_field=_LAST_CHECKED_FIELD,
    last_updated_field=_LAST_UPDATED_FIELD,
):
    args = parse_args()

    if args.debug:
        http.enable_debug()

    while True:
        try:
            threshold = (
                datetime.timedelta(0) if args.force else _MODEL_TO_THRESHOLD[model]
            )
            run_update(
                sessionmaker(bind=db.create_engine())(),
                model,
                api_cls,
                refresh_func,
                threshold_func,
                threshold,
                last_checked_field,
                last_updated_field,
                dry_run=args.dry_run,
            )
            break
        except Exception as e:
            traceback.print_exception(e)
            print(f"Retrying in {_SEC_WAIT_ON_FAIL} seconds...")
            time.sleep(_SEC_WAIT_ON_FAIL)
            continue


def directors_main():
    main(models.Director, dir_obj.Director, refresh_director, director_threshold)


def films_main():
    main(models.Film, film_obj.Film, refresh_film, film_threshold)


def offers_main():
    main(
        models.Film,
        film_obj.Film,
        refresh_offers,
        offer_threshold,
        "last_offers_checked",
        "last_offers_updated",
    )
