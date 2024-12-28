from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ArrayOfReportsItemSectionsItemFilmsItemDirectorsItem")


@_attrs_define
class ArrayOfReportsItemSectionsItemFilmsItemDirectorsItem:
    """
    Attributes:
        id (int):
        name (str):
        lb_url (Union[Unset, str]):
    """

    id: int
    name: str
    lb_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        lb_url = self.lb_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
            }
        )
        if lb_url is not UNSET:
            field_dict["lb_url"] = lb_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        lb_url = d.pop("lb_url", UNSET)

        array_of_reports_item_sections_item_films_item_directors_item = cls(
            id=id,
            name=name,
            lb_url=lb_url,
        )

        array_of_reports_item_sections_item_films_item_directors_item.additional_properties = d
        return array_of_reports_item_sections_item_films_item_directors_item

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
