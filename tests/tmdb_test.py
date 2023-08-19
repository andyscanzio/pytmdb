import os

import pytest

from pytmdb.tmdb import TMDB


def test_tmdb():
    with pytest.raises(ValueError) as excinfo:
        _ = TMDB(version=4)

    assert "Only version 3 supported" == str(excinfo.value)


def test_tmdb_without_key():
    tmdb = TMDB()
    assert tmdb.key is not None


def test_tmdb_with_wrong_key():
    with pytest.raises(ValueError) as excinfo:
        _ = TMDB(api_key="aa")

    assert "API KEY is not valid" == str(excinfo.value)


def test_tmdb_no_key():
    key = os.environ.get("TMDB_API_KEY", None)
    del os.environ["TMDB_API_KEY"]

    with pytest.raises(ValueError) as excinfo:
        _ = TMDB()

    assert "API KEY must be set" == str(excinfo.value)

    if isinstance(key, str):
        os.environ["TMDB_API_KEY"] = key
