from __future__ import annotations

import pytest

from pytmdb.models import SearchCollection
from pytmdb.models import SearchCompany
from pytmdb.models import SearchKeyword
from pytmdb.models import SearchPerson
from pytmdb.search import Search
from pytmdb.tmdb import TMDB

from .search_data import search_collection_expected
from .search_data import search_company_expected
from .search_data import search_keyword_expected
from .search_data import search_person_expected


@pytest.fixture(scope="session", name="tmdb")
def init_tmdb():
    return TMDB()


@pytest.fixture(scope="session", name="search")
def init_search(tmdb: TMDB):
    return Search(tmdb)


@pytest.mark.parametrize("input, expected", search_person_expected)
def test_search_person(search: Search, input: str, expected: list[SearchPerson]):
    inp = sorted(search.search_person(input))
    exp = sorted(expected)
    assert inp == exp
    for a, b in zip(inp, exp):
        assert sorted(a.known_for) == sorted(b.known_for)


@pytest.mark.parametrize("input, expected", search_collection_expected)
def test_search_collection(
    search: Search, input: str, expected: list[SearchCollection]
):
    inp = sorted(search.search_collection(input))
    exp = sorted(expected)
    assert inp == exp


@pytest.mark.parametrize("input, expected", search_company_expected)
def test_search_company(search: Search, input: str, expected: list[SearchCompany]):
    inp = sorted(search.search_company(input))
    exp = sorted(expected)
    assert inp == exp


@pytest.mark.parametrize("input, expected", search_keyword_expected)
def test_search_keyword(search: Search, input: str, expected: list[SearchKeyword]):
    inp = sorted(search.search_keyword(input))
    exp = sorted(expected)
    assert inp == exp
