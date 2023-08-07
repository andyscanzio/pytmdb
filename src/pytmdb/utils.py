from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Sequence

if TYPE_CHECKING:
    from pytmdb.tmdb import ParamsType
    from pytmdb.tmdb import ParamType


def add_params(param: ParamsType, values: Sequence[tuple[str, ParamType]]):
    for key, value in values:
        if value is not None:
            param[key] = value
    return param
