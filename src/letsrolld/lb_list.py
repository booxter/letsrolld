from bs4 import BeautifulSoup

from letsrolld.base import BaseObject
from letsrolld import film
from letsrolld import http


class MovieList(BaseObject):
    @property
    def film_urls(self):
        for page in range(1, 10000):
            print(f"Fetching page {page}")
            url = f"{self.url}/page/{page}/"

            while True:
                try:
                    content = http.get_url(url)
                    break
                except Exception as e:
                    print(f"Failed to fetch {url}: {e}")
                    continue

            soup = BeautifulSoup(content, "html.parser")

            found = False
            for movie in soup.find_all("div", class_="film-poster"):
                yield movie.get("data-target-link")
                found = True

            # if no movies were found, we're done
            if not found:
                break

    def films(self):
        for url in self.film_urls:
            yield film.Film(url)


class MovieCountryList(BaseObject):
    def __init__(self, country):
        url = f"https://letterboxd.com/films/ajax/popular/country/{country}"
        super().__init__(url)
        self._country = country

    @property
    def film_urls(self):
        for page in range(1, 10000):
            print(f"Fetching page {page}")
            url = f"{self.url}/page/{page}/"

            while True:
                try:
                    content = http.get_url(url)
                    break
                except Exception as e:
                    print(f"Failed to fetch {url}: {e}")
                    continue

            soup = BeautifulSoup(content, "html.parser")

            found = False
            for movie in soup.find_all("div", class_="film-poster"):
                yield "https://letterboxd.com" + movie.get("data-target-link")
                found = True

            # if no movies were found, we're done
            if not found:
                break

    def films(self):
        for url in self.film_urls:
            yield film.Film(url)
