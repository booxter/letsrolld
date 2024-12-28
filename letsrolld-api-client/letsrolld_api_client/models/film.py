from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.film_countries_item import FilmCountriesItem
    from ..models.film_directors_item import FilmDirectorsItem
    from ..models.film_offers_item import FilmOffersItem


T = TypeVar("T", bound="Film")


@_attrs_define
class Film:
    """
    Attributes:
        title (str):
        id (Union[Unset, int]):
        description (Union[Unset, str]):
        year (Union[None, Unset, int]):
        rating (Union[Unset, str]):
        runtime (Union[None, Unset, int]):
        lb_url (Union[Unset, str]):
        jw_url (Union[None, Unset, str]):
        trailer_url (Union[None, Unset, str]):
        genres (Union[Unset, list[str]]):
        countries (Union[Unset, list['FilmCountriesItem']]):
        offers (Union[Unset, list['FilmOffersItem']]):
        directors (Union[Unset, list['FilmDirectorsItem']]):
    """

    title: str
    id: Union[Unset, int] = UNSET
    description: Union[Unset, str] = UNSET
    year: Union[None, Unset, int] = UNSET
    rating: Union[Unset, str] = UNSET
    runtime: Union[None, Unset, int] = UNSET
    lb_url: Union[Unset, str] = UNSET
    jw_url: Union[None, Unset, str] = UNSET
    trailer_url: Union[None, Unset, str] = UNSET
    genres: Union[Unset, list[str]] = UNSET
    countries: Union[Unset, list["FilmCountriesItem"]] = UNSET
    offers: Union[Unset, list["FilmOffersItem"]] = UNSET
    directors: Union[Unset, list["FilmDirectorsItem"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        id = self.id

        description = self.description

        year: Union[None, Unset, int]
        if isinstance(self.year, Unset):
            year = UNSET
        else:
            year = self.year

        rating = self.rating

        runtime: Union[None, Unset, int]
        if isinstance(self.runtime, Unset):
            runtime = UNSET
        else:
            runtime = self.runtime

        lb_url = self.lb_url

        jw_url: Union[None, Unset, str]
        if isinstance(self.jw_url, Unset):
            jw_url = UNSET
        else:
            jw_url = self.jw_url

        trailer_url: Union[None, Unset, str]
        if isinstance(self.trailer_url, Unset):
            trailer_url = UNSET
        else:
            trailer_url = self.trailer_url

        genres: Union[Unset, list[str]] = UNSET
        if not isinstance(self.genres, Unset):
            genres = self.genres

        countries: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.countries, Unset):
            countries = []
            for countries_item_data in self.countries:
                countries_item = countries_item_data.to_dict()
                countries.append(countries_item)

        offers: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.offers, Unset):
            offers = []
            for offers_item_data in self.offers:
                offers_item = offers_item_data.to_dict()
                offers.append(offers_item)

        directors: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.directors, Unset):
            directors = []
            for directors_item_data in self.directors:
                directors_item = directors_item_data.to_dict()
                directors.append(directors_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if description is not UNSET:
            field_dict["description"] = description
        if year is not UNSET:
            field_dict["year"] = year
        if rating is not UNSET:
            field_dict["rating"] = rating
        if runtime is not UNSET:
            field_dict["runtime"] = runtime
        if lb_url is not UNSET:
            field_dict["lb_url"] = lb_url
        if jw_url is not UNSET:
            field_dict["jw_url"] = jw_url
        if trailer_url is not UNSET:
            field_dict["trailer_url"] = trailer_url
        if genres is not UNSET:
            field_dict["genres"] = genres
        if countries is not UNSET:
            field_dict["countries"] = countries
        if offers is not UNSET:
            field_dict["offers"] = offers
        if directors is not UNSET:
            field_dict["directors"] = directors

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.film_countries_item import FilmCountriesItem
        from ..models.film_directors_item import FilmDirectorsItem
        from ..models.film_offers_item import FilmOffersItem

        d = src_dict.copy()
        title = d.pop("title")

        id = d.pop("id", UNSET)

        description = d.pop("description", UNSET)

        def _parse_year(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        year = _parse_year(d.pop("year", UNSET))

        rating = d.pop("rating", UNSET)

        def _parse_runtime(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        runtime = _parse_runtime(d.pop("runtime", UNSET))

        lb_url = d.pop("lb_url", UNSET)

        def _parse_jw_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        jw_url = _parse_jw_url(d.pop("jw_url", UNSET))

        def _parse_trailer_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        trailer_url = _parse_trailer_url(d.pop("trailer_url", UNSET))

        genres = cast(list[str], d.pop("genres", UNSET))

        countries = []
        _countries = d.pop("countries", UNSET)
        for countries_item_data in _countries or []:
            countries_item = FilmCountriesItem.from_dict(countries_item_data)

            countries.append(countries_item)

        offers = []
        _offers = d.pop("offers", UNSET)
        for offers_item_data in _offers or []:
            offers_item = FilmOffersItem.from_dict(offers_item_data)

            offers.append(offers_item)

        directors = []
        _directors = d.pop("directors", UNSET)
        for directors_item_data in _directors or []:
            directors_item = FilmDirectorsItem.from_dict(directors_item_data)

            directors.append(directors_item)

        film = cls(
            title=title,
            id=id,
            description=description,
            year=year,
            rating=rating,
            runtime=runtime,
            lb_url=lb_url,
            jw_url=jw_url,
            trailer_url=trailer_url,
            genres=genres,
            countries=countries,
            offers=offers,
            directors=directors,
        )

        film.additional_properties = d
        return film

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
