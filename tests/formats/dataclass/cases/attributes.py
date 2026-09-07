from collections.abc import Mapping
from typing import Dict, List, Set, Tuple

cases = [
    (int, False),
    (Set, False),
    (List, False),
    (Tuple, False),
    (Dict[str, int], False),
    (Dict, ((str,), dict, None, False)),
    (Dict[str, str], ((str,), dict, None, False)),
    (Mapping[str, str], ((str,), dict, None, False)),
    (dict[str, str], ((str,), dict, None, False)),
    (dict, ((str,), dict, None, False)),
]
