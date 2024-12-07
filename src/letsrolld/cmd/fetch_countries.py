import sys

from bs4 import BeautifulSoup

from letsrolld import http


def main():
    # fetch film list
    url = "https://letterboxd.com/countries/"
    content = http.get_url(url)

    soup = BeautifulSoup(content, "html.parser")

    countries_section = soup.find("div", class_="browse-countries")
    if countries_section is None:
        print("No countries section found")
        sys.exit(1)

    for a in countries_section.find_all("a"):
        href = a.get("href")
        if not href.startswith("/films/country/"):
            continue
        print(href.split("/")[-2])
