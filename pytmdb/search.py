from __future__ import annotations

from typing import Generic
from typing import Optional
from typing import Self
from typing import TypeVar

import requests
from pydantic import BaseModel

from pytmdb.tmdb import TMDB
from pytmdb.tmdb import ParamType


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


class SearchMovie(BaseModel):
    adult: int
    backdrop_path: Optional[str]
    genre_ids: list[int]
    id: int
    original_language: str
    original_title: Optional[str] = None
    overview: str
    popularity: float
    poster_path: Optional[str]
    release_date: Optional[str] = None
    title: Optional[str] = None
    video: Optional[bool] = None
    vote_average: float
    vote_count: int


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


class SearchPerson(BaseModel):
    adult: bool
    gender: int
    id: int
    known_for_department: str
    name: str
    original_name: str
    popularity: float
    profile_path: str | None
    known_for: list[SearchMovie]


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
        params: ParamType,
    ) -> list[T]:
        request = self.tmdb.get(url, params=params)
        response = SearchResponse[search_class].parse(request)

        value = [result for result in response.results]

        if response.total_pages != 1:
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
        include_adult: bool = False,
        language: str = "en-US",
        page: int = 1,
        region: Optional[str] = None,
    ) -> list[SearchCollection]:
        url = self.url + "collection?"
        params: ParamType = {
            "query": query,
            "include_adult": include_adult,
            "language": language,
            "page": page,
            "region": region,
        }

        return self._search_generic(SearchCollection, url, params)

    def search_person(
        self,
        query: str,
        include_adult: bool = False,
        language: str = "en-US",
        page: int = 1,
    ) -> list[SearchPerson]:
        url = self.url + "person?"
        params: ParamType = {
            "query": query,
            "include_adult": include_adult,
            "language": language,
            "page": page,
        }

        return self._search_generic(SearchPerson, url, params)
