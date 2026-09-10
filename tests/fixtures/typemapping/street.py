from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tests.fixtures.typemapping.city import City
    from tests.fixtures.typemapping.house import House


@dataclass
class Street:
    class Meta:
        global_type = False

    name: str
    city: City | None = None
    houses: list[House] = field(default_factory=list)
