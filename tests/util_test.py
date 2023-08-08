from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Sequence

import pytest

from pytmdb.utils import add_params

if TYPE_CHECKING:
    from pytmdb.tmdb import ParamsType
    from pytmdb.tmdb import ParamType


@pytest.mark.parametrize(
    ("input, expected"), [([("test", None)], {}), ([("test", 1)], {"test": 1})]
)
def test_add_params(input: Sequence[tuple[str, ParamType]], expected: ParamsType):
    assert add_params({}, input) == expected
