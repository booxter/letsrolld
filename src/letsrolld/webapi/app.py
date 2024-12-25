import json
import os

from flask import Flask
from flask_cors import CORS
from flask_restful_swagger_3 import Api, Resource, swagger, create_open_api_resource
from flask_sqlalchemy import SQLAlchemy

import pycountry
from sqlalchemy import or_
from sqlalchemy.sql.expression import func

from letsrolld import config as lconfig
from letsrolld import db
from letsrolld.db import models
from letsrolld import filmlist
from letsrolld.webapi import models as webapi_models

import logging

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)
logging.getLogger("sqlalchemy").setLevel(logging.DEBUG)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = db.get_db_uri()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # do I need this?
CORS(app)

db_ = SQLAlchemy(app)

_LICENSE = {
    "name": "GPL-3.0",
    "url": "https://www.gnu.org/licenses/gpl-3.0.html",
}

WATCHED_FILE = "data/watched.csv"


def _get_flag(country):
    getters = [
        pycountry.countries.lookup,
        lambda c: pycountry.countries.get(alpha_2=c),
        lambda c: pycountry.countries.get(alpha_3=c),
        lambda c: pycountry.historic_countries.get(alpha_2=c),
        lambda c: pycountry.historic_countries.get(alpha_3=c),
    ]

    countries = {
        "UK": "GB",
        "Czechoslovakia": "CZ",
    }
    for getter in getters:
        try:
            c = getter(countries.get(country, country))
            if c:
                return c.flag
        except LookupError:
            pass


# TODO: this is ugly; reimplement it as association proxy if possible
def _get_offers(session, f):
    return list(
        session.query(
            models.Offer.name, models.FilmOffer.url, models.Offer.monetization_type
        )
        .join(models.FilmOffer)
        .filter(models.FilmOffer.film_id == f.id)
        .all()
    )


def _get_film(session, f):
    countries = [
        webapi_models.Country(name=c.name, flag=_get_flag(c.name)) for c in f.countries
    ]
    offers = [
        webapi_models.Offer(
            name=name, url=url, monetization_type=str(monetization_type)
        )
        for name, url, monetization_type in _get_offers(session, f)
    ]
    return webapi_models.Film(
        id=f.id,
        title=f.title,
        description=f.description,
        year=f.year,
        rating=f"{f.rating:.2f}",
        runtime=f.runtime,
        lb_url=f.lb_url,
        jw_url=f.jw_url,
        trailer_url=f.trailer_url,
        genres=[g.name for g in f.genres],
        countries=countries,
        offers=offers,
        directors=[_get_director_info(d) for d in f.directors],
    )


def _get_report(sections=None):
    return webapi_models.Report(
        id=0,
        name="default",
        sections=sections or [],
    )


def _get_director(session, d):
    return webapi_models.Director(
        info=_get_director_info(d),
        films=[_get_film(session, f) for f in d.films],
    )


def _get_director_info(d):
    return webapi_models.DirectorInfo(
        id=d.id,
        name=d.name,
        lb_url=d.lb_url,
    )


class DirectorResource(Resource):
    @swagger.reorder_with(
        webapi_models.ArrayOfDirectors,
        description="Returns directors",
        summary="Get Directors",
    )
    @swagger.parameters(
        [
            {
                "name": "limit",
                "in": "query",
                "description": "Number of directors to return",
                "required": False,
                "schema": {"type": "integer", "default": 10},
            },
        ]
    )
    def get(self, _parser):
        args = _parser.parse_args()
        return [
            _get_director(db_.session, d)
            for d in db_.session.query(models.Director)
            .order_by(func.random())
            .limit(args["limit"])
        ], 200


class DirectorItemResource(Resource):
    @swagger.reorder_with(
        webapi_models.Director,
        description="Returns a director",
        summary="Get Director",
    )
    def get(self, id):
        d = db_.session.query(models.Director).filter(models.Director.id == id).one()
        if d is None:
            return {}, 404
        return _get_director(db_.session, d), 200


class FilmResource(Resource):
    @swagger.reorder_with(
        webapi_models.ArrayOfFilms,
        description="Returns films",
        summary="Get Films",
    )
    @swagger.parameters(
        [
            {
                "name": "limit",
                "in": "query",
                "description": "Number of films to return",
                "required": False,
                "schema": {"type": "integer", "default": 10},
            },
            {
                "name": "genre",
                "in": "query",
                "description": "Genre to filter by",
                "required": False,
                "schema": {"type": "string"},
            },
            {
                "name": "country",
                "in": "query",
                "description": "Country to filter by",
                "required": False,
                "schema": {"type": "string"},
            },
            {
                "name": "offer",
                "in": "query",
                "description": "Offer to filter by",
                "required": False,
                "schema": {"type": "string"},
            },
        ]
    )
    def get(self, _parser):
        args = _parser.parse_args()

        query = db_.session.query(models.Film)
        if args["genre"]:
            genres = args["genre"].split(",")
            query = query.join(models.Film.genres).filter(models.Genre.name.in_(genres))
        if args["country"]:
            countries = args["country"].split(",")
            query = query.join(models.Film.countries).filter(
                models.Country.name.in_(countries)
            )
        if args["offer"]:
            offers = args["offer"].split(",")
            query = query.join(models.Film.offers).filter(models.Offer.name.in_(offers))

        query = query.order_by(func.random()).limit(args["limit"])
        return [_get_film(db_.session, d) for d in query], 200


class FilmItemResource(Resource):
    @swagger.reorder_with(
        webapi_models.Film, description="Returns a film", summary="Get Film"
    )
    def get(self, id):
        f = db_.session.query(models.Film).filter(models.Film.id == id).one()
        if f is None:
            return {}, 404
        return _get_film(db_.session, f), 200


def _get_report_config(id):
    # TODO: store configs in db; convert id into actual name
    return list(lconfig.from_file(os.path.join("configs", "default.json")))


# TODO: support freeform text search filter
def _execute_section_plan(db, config, seen_films):
    query = db.session.query(models.Film).filter(~models.Film.id.in_(seen_films))

    if config.min_rating:
        query = query.filter(models.Film.rating >= config.min_rating)
    if config.max_rating:
        query = query.filter(models.Film.rating <= config.max_rating)

    if config.min_length:
        query = query.filter(models.Film.runtime >= config.min_length)
    if config.max_length:
        query = query.filter(models.Film.runtime <= config.max_length)

    if config.genre:
        # TODO: support multiple genres filter
        query = query.join(models.Film.genres).filter(models.Genre.name == config.genre)
    if config.exclude_genres:
        query = query.filter(
            ~models.Film.genres.any(models.Genre.name.in_(config.exclude_genres))
        )

    if config.country:
        # TODO: support multiple countries filter
        query = query.join(models.Film.countries).filter(
            models.Country.name == config.country
        )
    if config.exclude_countries:
        query = query.filter(
            ~models.Film.countries.any(
                models.Country.name.in_(config.exclude_countries)
            )
        )

    if config.services:
        query = query.join(models.Film.offers).filter(
            or_(
                models.Offer.name.in_(config.services),
                models.Offer.monetization_type.in_(config.services),
            )
        )
    if config.exclude_services:
        query = query.join(models.Film.offers).filter(
            ~models.Film.offers.any(
                or_(
                    models.Offer.name.in_(config.exclude_services),
                    models.Offer.monetization_type.in_(config.exclude_services),
                )
            )
        )

    if config.min_year:
        query = query.filter(models.Film.year >= config.min_year)
    if config.max_year:
        query = query.filter(models.Film.year <= config.max_year)

    query = query.group_by(models.Film.lb_url).order_by(func.random())
    return [_get_film(db.session, f) for f in query.limit(config.max_movies)]


class ReportResource(Resource):
    @swagger.reorder_with(
        webapi_models.ArrayOfReports,
        description="Returns available reports",
        summary="List Reports",
    )
    def get(self):
        # TODO: actually list available reports
        return [_get_report()]


# TODO: store watched movied in db, per user
def _initialize_seen_movies(db):
    ids = set()
    films = [
        # TODO: handle invalid int conversion
        (f.name, int(f.year))
        for f in filmlist.read_film_list(WATCHED_FILE)
    ]

    # first, find all watched movies in a single query
    candidates = (
        db.session.query(models.Film)
        .filter(models.Film.title.in_([f[0] for f in films]))
        .all()
    )

    for candidate in candidates:
        if (candidate.title, candidate.year) in films:
            ids.add(candidate.id)
            films.remove((candidate.title, candidate.year))

    return ids


class ReportItemResource(Resource):
    @swagger.reorder_with(
        webapi_models.Report,
        description="Execute a report",
        summary="Execute Report",
    )
    def get(self, id):
        # TODO: support multiple reports
        if id != 0:
            return {}, 404
        sections = []
        seen_films = _initialize_seen_movies(db_)
        for config in _get_report_config(id):
            films = _execute_section_plan(db_, config, seen_films)
            seen_films.update(f["id"] for f in films)
            sections.append(webapi_models.ReportSection(name=config.name, films=films))
        return _get_report(sections=sections), 200


def _api():
    api = Api(app, title="letsrolld API", license=_LICENSE, version="0.1")

    # TODO: generalize endpoint definitions
    api.add_resource(DirectorResource, "/directors")
    api.add_resource(DirectorItemResource, "/directors/<int:id>")

    api.add_resource(FilmResource, "/films")
    api.add_resource(FilmItemResource, "/films/<int:id>")

    # TODO: support different ids
    # TODO: store report rules in db
    api.add_resource(ReportResource, "/reports")
    api.add_resource(ReportItemResource, "/reports/<int:id>")

    return api


def main():
    _ = _api()
    # app.run(port=8000, debug=True)
    app.run(port=8000, debug=False)


def swagger_json():
    api = _api()
    with app.test_request_context():
        swagger_doc = create_open_api_resource(api.open_api_object)().get()
    print(json.dumps(swagger_doc, indent=4, sort_keys=False))
