from collections import namedtuple
import functools
import re
import urllib.parse

from bs4 import BeautifulSoup

from letsrolld import director
from letsrolld import http
from letsrolld import justwatch as jw
from letsrolld.base import BaseObject


Offer = namedtuple("Offer", ["technical_name", "url", "monetization_type"])


class Film(BaseObject):
    def __init__(self, url):
        super().__init__(url)
        self._jw = None
        self._jw_fetched = False
        self._avail_soup = None

    @functools.cached_property
    def jw(self):
        if not self._jw_fetched:
            self._jw = jw.get_title(self.jw_url)
            self._jw_fetched = True
        return self._jw

    @functools.cached_property
    def offers(self):
        return [] if self.jw is None else self.jw.offers

    @functools.cached_property
    def genres(self):
        genres = [] if self.jw is None else self.jw.genres
        if self.soup.find("span", class_="badge -adult"):
            genres.append("adult")
        return genres

    @functools.cached_property
    def genre_names(self):
        return "" if not self.genres else ",".join(self.genres)

    def __eq__(self, other):
        return (
            self.name == other.name
            and self.year == other.year
            and self.rating == other.rating
        )

    @functools.cached_property
    def description(self):
        return self.lb_description if self.jw is None else self.jw.short_description

    @property
    def lb_description(self):
        snippets = []
        description = self.soup.find("meta", property="og:description")
        if description:
            snippets.append(description.get("content"))
        tagline = self.soup.find("h4", class_="tagline")
        if tagline:
            snippets.append(tagline.text.strip())
        return " ".join(snippets)

    @functools.cached_property
    def avail_soup(self):
        if self._avail_soup is None:
            url = urllib.parse.urljoin(
                self.url.replace("letterboxd.com", "letterboxd.com/csi"),
                "availability/",
            )
            self._avail_soup = BeautifulSoup(http.get_url(url), "html.parser")
        return self._avail_soup

    def available_physical(self):
        for x in self.avail_soup.find_all("p", class_="service -amazon"):
            return True
        return False

    @property
    def available_services(self):
        services = [
            # TODO: confirm that api returns one of the known monetization types
            Offer(
                technical_name=offer.package.technical_name,
                url=offer.url,
                monetization_type=offer.monetization_type,
            )
            for offer in self.offers
        ]
        if self.available_physical():
            # TODO: use const for monetization type
            services.append(
                Offer(technical_name="physical", url=None, monetization_type="DISC")
            )
        return services

    @functools.cached_property
    def jw_url(self):
        for x in self.avail_soup.find_all("a", class_="jw-branding"):
            link = x.get("href")
            if not link.startswith("https://www.justwatch.com/us/"):
                return None
            return link

    @functools.cached_property
    def multi_episode(self):
        if not self._jw_runtime:
            return False
        if not self._lb_runtime:
            return False
        # heuristic is: if runtimes are vastly different, it's a series
        # though we usually only see jw runtime shorter, handle both
        return ((self._lb_runtime / self._jw_runtime) > 1.5) or (
            (self._jw_runtime / self._lb_runtime) > 1.5
        )

    @functools.cached_property
    def _lb_runtime(self):
        for p in self.soup.find_all("p", class_="text-link text-footer"):
            match = re.search(r"(\d+)\smins", p.text)
            if match:
                return int(match.group(1))

    @functools.cached_property
    def _jw_runtime(self):
        if self.jw is not None:
            return self.jw.runtime_minutes

    @functools.cached_property
    def runtime(self):
        jw_runtime = self._jw_runtime
        lb_runtime = self._lb_runtime
        if self.multi_episode:
            return max(jw_runtime, lb_runtime)
        # prefer jw runtime if available
        return jw_runtime or lb_runtime

    @functools.cached_property
    def _full_title(self):
        return (
            # TODO: extract name and year from the body?
            self.soup.title.string.split(" directed by")[0]
            .strip()
            .replace("\u200e", "")
        )

    @functools.cached_property
    def name(self):
        pattern = r"^(.*?)\s*\(\d{4}\)"
        match = re.search(pattern, self._full_title)
        if match:
            return match.group(1).strip()
        return self._full_title

    # TODO: switch to int
    @functools.cached_property
    def year(self):
        pattern = r"\((\d{4})\)"
        match = re.search(pattern, self._full_title)
        if match:
            return match.group(1).strip()

    def _get_director_slugs(self):
        for crew in self.soup.find_all(id="tab-crew"):
            for h3 in crew.find_all("h3"):
                text = h3.text.strip()
                if "Director\n" in text or "Directors\n" in text:
                    text_slug = h3.next_sibling.next_sibling
                    return text_slug.find_all("a")
        return []

    @property
    def trailer_url(self):
        for a in self.soup.find_all("a", class_="play track-event js-video-zoom"):
            href = a.get("href")
            if href:
                yt_id = href.split("/")[4].split("?")[0]
                return f"https://www.youtube.com/watch?v={yt_id}"

    @property
    def countries(self):
        countries = []
        for details in self.soup.find_all(id="tab-details"):
            for h3 in details.find_all("h3"):
                text = h3.text.strip()
                if "Country" in text or "Countries" in text:
                    text_slug = h3.next_sibling.next_sibling
                    for a in text_slug.find_all("a"):
                        countries.append(a.text.strip())
        return countries

    @functools.cached_property
    def directors(self):
        return [
            director.Director(url=a.get("href")) for a in self._get_director_slugs()
        ]

    @functools.cached_property
    def director_names(self):
        return ", ".join(a.text.strip() for a in self._get_director_slugs())

    # TODO: calculate my own rating for movies without a rating
    # TODO: pull rating from imdb too
    @functools.cached_property
    def rating(self):
        # TODO: parse as json
        for script in self.soup.find_all("script"):
            if "ratingValue" in script.text:
                return (
                    script.text.split("ratingValue")[1]
                    .split(":")[1]
                    .split(",")[0]
                    .strip()
                )
        return "0"
