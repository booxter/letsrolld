from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.array_of_films_item import ArrayOfFilmsItem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: Union[Unset, int] = 10,
    genre: Union[Unset, str] = UNSET,
    country: Union[Unset, str] = UNSET,
    offer: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    params["genre"] = genre

    params["country"] = country

    params["offer"] = offer

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/films",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["ArrayOfFilmsItem"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_array_of_films_item_data in _response_200:
            componentsschemas_array_of_films_item = ArrayOfFilmsItem.from_dict(
                componentsschemas_array_of_films_item_data
            )

            response_200.append(componentsschemas_array_of_films_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["ArrayOfFilmsItem"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 10,
    genre: Union[Unset, str] = UNSET,
    country: Union[Unset, str] = UNSET,
    offer: Union[Unset, str] = UNSET,
) -> Response[list["ArrayOfFilmsItem"]]:
    """Get Films

    Args:
        limit (Union[Unset, int]):  Default: 10.
        genre (Union[Unset, str]):
        country (Union[Unset, str]):
        offer (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ArrayOfFilmsItem']]
    """

    kwargs = _get_kwargs(
        limit=limit,
        genre=genre,
        country=country,
        offer=offer,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 10,
    genre: Union[Unset, str] = UNSET,
    country: Union[Unset, str] = UNSET,
    offer: Union[Unset, str] = UNSET,
) -> Optional[list["ArrayOfFilmsItem"]]:
    """Get Films

    Args:
        limit (Union[Unset, int]):  Default: 10.
        genre (Union[Unset, str]):
        country (Union[Unset, str]):
        offer (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ArrayOfFilmsItem']
    """

    return sync_detailed(
        client=client,
        limit=limit,
        genre=genre,
        country=country,
        offer=offer,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 10,
    genre: Union[Unset, str] = UNSET,
    country: Union[Unset, str] = UNSET,
    offer: Union[Unset, str] = UNSET,
) -> Response[list["ArrayOfFilmsItem"]]:
    """Get Films

    Args:
        limit (Union[Unset, int]):  Default: 10.
        genre (Union[Unset, str]):
        country (Union[Unset, str]):
        offer (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ArrayOfFilmsItem']]
    """

    kwargs = _get_kwargs(
        limit=limit,
        genre=genre,
        country=country,
        offer=offer,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 10,
    genre: Union[Unset, str] = UNSET,
    country: Union[Unset, str] = UNSET,
    offer: Union[Unset, str] = UNSET,
) -> Optional[list["ArrayOfFilmsItem"]]:
    """Get Films

    Args:
        limit (Union[Unset, int]):  Default: 10.
        genre (Union[Unset, str]):
        country (Union[Unset, str]):
        offer (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ArrayOfFilmsItem']
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            genre=genre,
            country=country,
            offer=offer,
        )
    ).parsed
