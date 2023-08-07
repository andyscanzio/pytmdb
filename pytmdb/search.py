from __future__ import annotations

from typing import TYPE_CHECKING
from typing import TypeVar

import requests

from pytmdb.models import SearchCollection
from pytmdb.models import SearchCompany
from pytmdb.models import SearchPerson
from pytmdb.models import SearchResponse
from pytmdb.utils import add_params

if TYPE_CHECKING:
    from pytmdb.tmdb import TMDB
    from pytmdb.tmdb import ParamsType


T = TypeVar("T")


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
        response = SearchResponse[search_class].parse(request)  # type: ignore

        value = [result for result in response.results]

        if page is None and response.total_pages != 1:
            for i in range(1, response.total_pages):
                params["page"] = i + 1
                request = requests.get(url, params=params, headers=self.tmdb.header)
                response = SearchResponse[search_class].parse(request)  # type: ignore
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
        return [SearchCompany(id=1, logo_path="a", origin_country="a", name="a")]

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
