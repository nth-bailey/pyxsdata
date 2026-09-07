from collections.abc import Iterable, Sequence
from typing import Dict, List, Literal, Optional, Set, Tuple, Union

from pyxsdata.models.enums import Mode

tokens = [
    (int, False),
    (Dict[int, int], False),
    (Dict, False),
    (Literal["foo"], False),
    (Set[str], False),
    (List[Union[List[int], int]], False),
    (List[List[int]], False),
    (Tuple[int, ...], ((int,), None, tuple, False)),
    (Iterable[int], ((int,), None, list, False)),
    (Sequence[int], ((int,), None, list, False)),
    (List[int], ((int,), None, list, False)),
    (List[Union[str, int]], ((str, int), None, list, False)),
    (Optional[List[Union[str, int]]], ((str, int), None, list, True)),
    (list[int, int], False),
    (dict[str, str], False),
    (dict, False),
    (set[str], False),
    (tuple[int, ...], ((int,), None, tuple, False)),
    (list[int], ((int,), None, list, False)),
    (list[Union[str, int]], ((str, int), None, list, False)),
    (tuple[int | str], ((int, str), None, tuple, False)),
]

not_tokens = [
    (List[int], False),
    (Dict[int, str], False),
    (int, ((int,), None, None, False)),
    (str, ((str,), None, None, False)),
    (Union[str, Mode], ((str, Mode), None, None, False)),
    (int | str, ((int, str), None, None, False)),
]
