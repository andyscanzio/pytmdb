import pytest

from pytmdb.tmdb import TMDB


def test_tmdb_version():
    with pytest.raises(ValueError) as excinfo:
        _ = TMDB(version=4)

    assert "Only version 3 supported" == str(excinfo.value)


def test_tmdb_without_key():
    tmdb = TMDB()
    assert tmdb.key is not None


def test_tmdb_with_key():
    tmdb = TMDB(api_key="aa")
    assert tmdb.key is not None
