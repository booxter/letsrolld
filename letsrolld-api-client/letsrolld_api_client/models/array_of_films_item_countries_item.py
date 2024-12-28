from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ArrayOfFilmsItemCountriesItem")


@_attrs_define
class ArrayOfFilmsItemCountriesItem:
    """
    Attributes:
        name (str):
        flag (Union[None, Unset, str]):
    """

    name: str
    flag: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        flag: Union[None, Unset, str]
        if isinstance(self.flag, Unset):
            flag = UNSET
        else:
            flag = self.flag

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if flag is not UNSET:
            field_dict["flag"] = flag

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        def _parse_flag(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        flag = _parse_flag(d.pop("flag", UNSET))

        array_of_films_item_countries_item = cls(
            name=name,
            flag=flag,
        )

        array_of_films_item_countries_item.additional_properties = d
        return array_of_films_item_countries_item

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
