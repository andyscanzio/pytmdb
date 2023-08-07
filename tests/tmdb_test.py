import pytest

from pytmdb.tmdb import TMDB


def test_tmdb():
    with pytest.raises(ValueError) as excinfo:
        _ = TMDB(version=4)

    assert "Only version 3 supported" == str(excinfo.value)
