from __future__ import annotations

import requests

ParamType = str | bool | int | None
ParamsType = dict[str, ParamType]


class TMDB:
    def __init__(self, version: int = 3):
        self.url = "https://api.themoviedb.org"
        if version == 3:
            self.url += "/3/"
        else:
            raise ValueError("Only version 3 supported")
        self.header = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5ZThkMGYzYzYwZmExM2ZiNjEyNjhiMjA0Y2E3Y2Y0ZSIsInN1YiI6IjY0Y2U2NWNlNmQ0Yzk3MDEwZDUwNzVmNCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.cN5wSn0EN0w4EHFyDKsMn6Akk6hTcfFwGO1I0Fu_MLA",  # noqa:E501
        }

    def get(self, url: str, params: ParamsType) -> requests.Response:
        return requests.get(url, params=params, headers=self.header)
