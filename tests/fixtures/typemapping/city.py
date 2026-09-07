from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tests.fixtures.typemapping.street import Street


@dataclass
class City:
    class Meta:
        global_type = False

    name: str
    streets: list["Street"] = field(default_factory=list)
