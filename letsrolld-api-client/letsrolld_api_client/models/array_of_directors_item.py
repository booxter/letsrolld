from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.array_of_directors_item_films_item import ArrayOfDirectorsItemFilmsItem
    from ..models.array_of_directors_item_info import ArrayOfDirectorsItemInfo


T = TypeVar("T", bound="ArrayOfDirectorsItem")


@_attrs_define
class ArrayOfDirectorsItem:
    """
    Attributes:
        info (ArrayOfDirectorsItemInfo):
        films (Union[Unset, list['ArrayOfDirectorsItemFilmsItem']]):
    """

    info: "ArrayOfDirectorsItemInfo"
    films: Union[Unset, list["ArrayOfDirectorsItemFilmsItem"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        info = self.info.to_dict()

        films: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.films, Unset):
            films = []
            for films_item_data in self.films:
                films_item = films_item_data.to_dict()
                films.append(films_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "info": info,
            }
        )
        if films is not UNSET:
            field_dict["films"] = films

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.array_of_directors_item_films_item import ArrayOfDirectorsItemFilmsItem
        from ..models.array_of_directors_item_info import ArrayOfDirectorsItemInfo

        d = src_dict.copy()
        info = ArrayOfDirectorsItemInfo.from_dict(d.pop("info"))

        films = []
        _films = d.pop("films", UNSET)
        for films_item_data in _films or []:
            films_item = ArrayOfDirectorsItemFilmsItem.from_dict(films_item_data)

            films.append(films_item)

        array_of_directors_item = cls(
            info=info,
            films=films,
        )

        array_of_directors_item.additional_properties = d
        return array_of_directors_item

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
