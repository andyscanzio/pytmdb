from __future__ import annotations

from dataclasses import field
from typing import Generic
from typing import Optional
from typing import Self
from typing import TypeVar

import requests
from pydantic import BaseModel
from pydantic.dataclasses import dataclass

T = TypeVar("T")


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


class SearchResponse(BaseModel, Generic[T]):
    page: int
    total_pages: int
    total_results: int
    results: list[T]

    @classmethod
    def parse(cls, response: requests.Response) -> Self:
        return cls(**response.json())
