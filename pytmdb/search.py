from __future__ import annotations

from dataclasses import field
from typing import TYPE_CHECKING
from typing import Generic
from typing import Optional
from typing import Self
from typing import TypeVar

import requests
from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from pytmdb.tmdb import TMDB
from pytmdb.utils import add_params

if TYPE_CHECKING:
    from pytmdb.tmdb import ParamsType


class SearchCollection(BaseModel):
    adult: bool
    backdrop_path: Optional[str]
    id: int
    name: str
    original_language: str
    original_name: str
    overview: str
    poster_path: Optional[str]


class SearchCompany(BaseModel):
    id: int
    logo_path: str
    name: str
    origin_country: str


class SearchKeyword(BaseModel):
    id: int
    name: str


@dataclass(order=True)
class SearchMovie:
    adult: int = field(repr=False, compare=True)
    backdrop_path: Optional[str] = field(repr=False, compare=False)
    genre_ids: list[int] = field(repr=False, compare=True)
    id: int = field(repr=True, compare=True)
    original_language: str = field(repr=False, compare=True)
    overview: str = field(repr=False, compare=True)
    popularity: float = field(repr=False, compare=False)
    poster_path: Optional[str] = field(repr=False, compare=False)
    vote_average: float = field(repr=False, compare=False)
    vote_count: int = field(repr=False, compare=False)
    original_title: Optional[str] = field(
        default=None, repr=False, compare=False
    )
    release_date: Optional[str] = field(
        default=None, repr=False, compare=False
    )
    title: Optional[str] = field(default=None, repr=True, compare=False)
    video: Optional[bool] = field(default=None, repr=False, compare=False)


class SearchMulti(BaseModel):
    adult: bool
    backdrop_path: Optional[str]
    id: int
    title: str
    original_language: str
    original_title: str
    overview: str
    poster_path: str
    media_type: str
    genre_ids: list[int]
    popularity: float
    release_date: str
    video: bool
    vote_average: float
    vote_count: int


@dataclass(order=True)
class SearchPerson:
    adult: bool = field(repr=False, compare=True)
    gender: int = field(repr=False, compare=True)
    id: int = field(repr=True, compare=True)
    known_for_department: str = field(repr=False, compare=True)
    name: str = field(repr=True, compare=True)
    original_name: str = field(repr=False, compare=True)
    popularity: float = field(repr=False, compare=False)
    profile_path: str | None = field(repr=False, compare=False)
    known_for: list[SearchMovie] = field(repr=True, compare=False)


class SearchTV(BaseModel):
    adult: bool
    backdrop_path: Optional[str]
    genre_ids: list[int]
    id: int
    origin_country: list[str]
    original_language: str
    original_name: str
    overview: str
    popularity: float
    poster_path: str
    first_air_date: str
    name: str
    vote_average: float
    vote_count: int


T = TypeVar("T")


class SearchResponse(BaseModel, Generic[T]):
    page: int
    total_pages: int
    total_results: int
    results: list[T]

    @classmethod
    def parse(cls, response: requests.Response) -> Self:
        return cls(**response.json())


class Search:
    def __init__(self, tmdb: TMDB):
        self.tmdb = tmdb
        self.url = self.tmdb.url + "search/"

    def _search_generic(
        self,
        search_class: type[T],
        url: str,
        params: ParamsType,
        page: int | None,
    ) -> list[T]:
        request = self.tmdb.get(url, params=params)
        response = SearchResponse[search_class].parse(request)

        value = [result for result in response.results]

        if page is None and response.total_pages != 1:
            for i in range(1, response.total_pages):
                params["page"] = i + 1
                request = requests.get(
                    url, params=params, headers=self.tmdb.header
                )
                response = SearchResponse[search_class].parse(request)
                value.extend(result for result in response.results)

        return value

    def search_collection(
        self,
        query: str,
        include_adult: bool | None = None,
        language: str | None = None,
        page: int | None = None,
        region: str | None = None,
    ) -> list[SearchCollection]:
        assert query is not None
        url = self.url + "collection?"
        params: ParamsType = {"query": query}
        params = add_params(
            params,
            (
                ("include_adult", include_adult),
                ("language", language),
                ("page", page),
                ("region", region),
            ),
        )

        return self._search_generic(SearchCollection, url, params, page)

    def search_company(self, query: str, page: int) -> list[SearchCompany]:
        return [
            SearchCompany(id=1, logo_path="a", origin_country="a", name="a")
        ]

    def search_person(
        self,
        query: str,
        include_adult: bool | None = None,
        language: str | None = None,
        page: int | None = None,
    ) -> list[SearchPerson]:
        assert query is not None
        url = self.url + "person?"
        params: ParamsType = {"query": query}

        params = add_params(
            params,
            (
                ("include_adult", include_adult),
                ("language", language),
                ("page", page),
            ),
        )
        return self._search_generic(SearchPerson, url, params, page)
