from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.array_of_reports_item_sections_item_films_item import ArrayOfReportsItemSectionsItemFilmsItem


T = TypeVar("T", bound="ArrayOfReportsItemSectionsItem")


@_attrs_define
class ArrayOfReportsItemSectionsItem:
    """
    Attributes:
        name (str):
        films (list['ArrayOfReportsItemSectionsItemFilmsItem']):
    """

    name: str
    films: list["ArrayOfReportsItemSectionsItemFilmsItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        films = []
        for films_item_data in self.films:
            films_item = films_item_data.to_dict()
            films.append(films_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "films": films,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.array_of_reports_item_sections_item_films_item import ArrayOfReportsItemSectionsItemFilmsItem

        d = src_dict.copy()
        name = d.pop("name")

        films = []
        _films = d.pop("films")
        for films_item_data in _films:
            films_item = ArrayOfReportsItemSectionsItemFilmsItem.from_dict(films_item_data)

            films.append(films_item)

        array_of_reports_item_sections_item = cls(
            name=name,
            films=films,
        )

        array_of_reports_item_sections_item.additional_properties = d
        return array_of_reports_item_sections_item

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
