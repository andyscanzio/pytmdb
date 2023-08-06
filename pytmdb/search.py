from typing import Generic
from typing import Optional
from typing import TypeVar

import requests
from pydantic import BaseModel

from .tmdb import TMDB


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


class SearchRequest(BaseModel, Generic[T]):
    page: int
    total_pages: int
    total_results: int
    results: list[T]


class Search:
    def __init__(self, tmdb: TMDB):
        self.tmdb = tmdb
        self.url = self.tmdb.url + "search/"

    def search_person(
        self,
        query: str,
        include_adult: bool = False,
        language: str = "en-US",
        page: int = 1,
    ) -> list[SearchPerson]:
        url = self.url + "person?"
        params = {
            "query": query,
            "include_adult": include_adult,
            "language": language,
            "page": page,
        }

        request = requests.get(url, params=params, headers=self.tmdb.header)
        response = SearchRequest[SearchPerson](**request.json())

        value = [result for result in response.results]

        if response.total_pages != 1:
            for i in range(1, response.total_pages):
                params["page"] = i + 1
                request = requests.get(
                    url, params=params, headers=self.tmdb.header
                )
                response = SearchRequest[SearchPerson](**request.json())
                value.extend(result for result in response.results)

        return value
