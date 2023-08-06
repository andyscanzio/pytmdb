import pytest

from pytmdb.search import Search
from pytmdb.search import SearchCollection
from pytmdb.search import SearchPerson
from pytmdb.tmdb import TMDB

from .search_data import search_collection_expected
from .search_data import search_person_expected


@pytest.fixture(scope="session", name="tmdb")
def init_tmdb():
    return TMDB()


@pytest.fixture(scope="session", name="search")
def init_search(tmdb: TMDB):
    return Search(tmdb)


@pytest.mark.parametrize("input, expected", search_person_expected)
def test_search_person(
    search: Search, input: str, expected: list[SearchPerson]
):
    assert search.search_person(input) == expected


@pytest.mark.parametrize("input, expected", search_collection_expected)
def test_search_collection(
    search: Search, input: str, expected: list[SearchCollection]
):
    assert search.search_collection(input) == expected
