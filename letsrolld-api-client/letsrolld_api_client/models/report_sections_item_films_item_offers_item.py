from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ReportSectionsItemFilmsItemOffersItem")


@_attrs_define
class ReportSectionsItemFilmsItemOffersItem:
    """
    Attributes:
        name (str):
        monetization_type (str):
        url (Union[None, str]):
    """

    name: str
    monetization_type: str
    url: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        monetization_type = self.monetization_type

        url: Union[None, str]
        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "monetization_type": monetization_type,
                "url": url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        monetization_type = d.pop("monetization_type")

        def _parse_url(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        url = _parse_url(d.pop("url"))

        report_sections_item_films_item_offers_item = cls(
            name=name,
            monetization_type=monetization_type,
            url=url,
        )

        report_sections_item_films_item_offers_item.additional_properties = d
        return report_sections_item_films_item_offers_item

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
