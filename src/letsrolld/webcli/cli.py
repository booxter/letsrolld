import click
from jinja2 import Environment, PackageLoader

from letsrolld_api_client import Client
from letsrolld_api_client.api.default import get_directors

# from letsrolld_api_client.api.default import get_directors_id
from letsrolld_api_client.api.default import get_films
# from letsrolld_api_client.api.default import get_films_id


DEFAULT_OFFERS = {
    # TODO: use constants for offer names
    "criterionchannel",
    "amazon",
    "kanopy",
    "hoopla",
    "amazonprime",
    "youtube",
}


# TODO: make the url configurable
client = Client(base_url="http://localhost:8000")


env = Environment(
    loader=PackageLoader("letsrolld.webcli"),
)


def list_film(film):
    template = env.get_template("film.template")
    return template.render(film=film)


def list_director(director):
    template = env.get_template("director.template")
    return template.render(director=director)


def report_film(film):
    template = env.get_template("film-full.template")
    return template.render(film=film, offers=DEFAULT_OFFERS)


@click.group()
def cli():
    pass


@cli.group()
def directors():
    pass


@directors.command(name="get")
def directors_get():
    global client
    with client as client:
        director_reports = []
        for director in get_directors.sync(client=client):
            director_reports.append(list_director(director))

    print("\n\n".join(director_reports))


@cli.group()
def films():
    pass


@films.command(name="get")
def films_get():
    global client
    with client as client:
        film_reports = []
        for film in get_films.sync(client=client):
            film_reports.append(list_film(film))

    print("\n".join(film_reports))


def _get_query_args(limit, genre, country, offer):
    args = {"limit": limit}
    if genre:
        args["genre"] = genre
    if country:
        args["country"] = country
    if offer:
        args["offer"] = offer
    return args


@films.command(name="query")
# TODO: build options from the API model definition
@click.option("--limit", default=10)
@click.option("--genre", default=None)
@click.option("--country", default=None)
@click.option("--offer", default=None)
def films_query(
        limit: int,
        genre: str,
        country: str,
        offer: str,
):
    global client
    with client as client:
        args = _get_query_args(limit, genre, country, offer)
        film_reports = []
        for film in get_films.sync(client=client, **args):
            film_reports.append(report_film(film))

    print("\n\n".join(film_reports))


if __name__ == "__main__":
    cli()
