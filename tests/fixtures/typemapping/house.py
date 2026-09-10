from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tests.fixtures.typemapping.street import Street


@dataclass
class House:
    class Meta:
        global_type = False

    number: int
    street: Street | None = None
