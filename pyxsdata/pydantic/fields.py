from typing import Any

from pydantic import fields
from pydantic_core import PydanticUndefined


class FieldInfo(fields.FieldInfo):  # ty: ignore[subclass-of-final-class]
    """Custom Pydantic FieldInfo carrying pyxsdata metadata."""

    __slots__ = ("xsdata_metadata",)

    def __init__(self, metadata: dict[str, Any] | None, **kwargs: Any):
        """Initialize FieldInfo with metadata."""
        super().__init__(**kwargs)
        self.xsdata_metadata = metadata


def field(
    metadata: dict[str, Any] | None = None,
    *,
    default: Any = PydanticUndefined,
    default_factory: Any = PydanticUndefined,
    **kwargs: Any,
) -> Any:
    """Create a Pydantic field configured with pyxsdata metadata."""
    return FieldInfo(
        metadata=metadata, default=default, default_factory=default_factory, **kwargs
    )
