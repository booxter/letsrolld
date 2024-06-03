import json

from flask import Flask
from flask_cors import CORS
from flask_restful_swagger_3 import Api, Resource, swagger, create_open_api_resource
from flask_sqlalchemy import SQLAlchemy

import pycountry
from sqlalchemy.sql.expression import func

from letsrolld import db
from letsrolld.db import models
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
        session.query(models.Offer.name, models.FilmOffer.url)
        .join(models.FilmOffer)
        .filter(models.FilmOffer.film_id == f.id)
        .all()
    )


def _get_film(session, f):
    countries = [
        webapi_models.Country(name=c.name, flag=_get_flag(c.name)) for c in f.countries
    ]
    offers = [
        webapi_models.Offer(name=name, url=url) for name, url in _get_offers(session, f)
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
            query = query.join(models.Film.genres).filter(
                models.Genre.name == args["genre"]
            )
        if args["country"]:
            query = query.join(models.Film.countries).filter(
                models.Country.name == args["country"]
            )
        if args["offer"]:
            query = query.join(models.Film.offers).filter(
                models.Offer.name == args["offer"]
            )

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


def _api():
    api = Api(app, title="letsrolld API", license=_LICENSE, version="0.1")

    # TODO: generalize endpoint definitions
    api.add_resource(DirectorResource, "/directors")
    api.add_resource(DirectorItemResource, "/directors/<int:id>")

    api.add_resource(FilmResource, "/films")
    api.add_resource(FilmItemResource, "/films/<int:id>")

    return api


def main():
    _ = _api()
    app.run(port=8000, debug=True)


def swagger_json():
    api = _api()
    with app.test_request_context():
        swagger_doc = create_open_api_resource(api.open_api_object)().get()
    print(json.dumps(swagger_doc, indent=4, sort_keys=False))
