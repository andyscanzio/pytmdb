import pytest

from pytmdb.models.search_models import SearchCollection
from pytmdb.models.search_models import SearchPerson
from pytmdb.search import Search
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
    inp = sorted(search.search_person(input))
    exp = sorted(expected)
    assert inp == exp
    for a, b in zip(inp, exp):
        assert sorted(a.known_for) == sorted(b.known_for)


@pytest.mark.parametrize("input, expected", search_collection_expected)
def test_search_collection(
    search: Search, input: str, expected: list[SearchCollection]
):
    assert search.search_collection(input) == expected
