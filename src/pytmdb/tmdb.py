from __future__ import annotations

import os
from typing import TYPE_CHECKING
from typing import Optional
from typing import Union

import requests

if TYPE_CHECKING:
    ParamType = Optional[Union[str, bool, int]]
    ParamsType = dict[str, ParamType]


class TMDB:
    def __init__(self, api_key: Optional[str] = None, version: int = 3):
        self.url = "https://api.themoviedb.org"
        if version == 3:
            self.url += "/3/"
        else:
            raise ValueError("Only version 3 supported")
        if api_key is None:
            self.key = os.environ.get("TMDB_API_KEY", None)
        else:
            self.key = api_key
        if self.key is None:
            raise ValueError("API KEY must be set")  # pragma: no cover
        self.header = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.key}",
        }

    def get(self, url: str, params: ParamsType) -> requests.Response:
        return requests.get(url, params=params, headers=self.header)
