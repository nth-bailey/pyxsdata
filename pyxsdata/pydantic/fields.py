from collections.abc import Callable
from typing import Any, overload

from pydantic import fields
from pydantic_core import PydanticUndefined


class FieldInfo(fields.FieldInfo):  # ty: ignore[subclass-of-final-class]
    """Custom Pydantic FieldInfo carrying pyxsdata metadata."""

    __slots__ = ("xsdata_metadata",)

    def __init__(self, metadata: dict[str, Any] | None, **kwargs: Any):
        """Initialize FieldInfo with metadata."""
        super().__init__(**kwargs)
        self.xsdata_metadata = metadata


@overload
def field[T](
    metadata: dict[str, Any] | None = ...,
    *,
    default: T,
    **kwargs: Any,
) -> T: ...


@overload
def field[T](
    metadata: dict[str, Any] | None = ...,
    *,
    default_factory: Callable[[], T],
    **kwargs: Any,
) -> T: ...


@overload
def field(
    metadata: dict[str, Any] | None = ...,
    **kwargs: Any,
) -> Any: ...


def field(
    metadata: dict[str, Any] | None = None,
    *,
    default: Any = PydanticUndefined,
    default_factory: Any = PydanticUndefined,
    **kwargs: Any,
) -> Any:
    """Create a Pydantic field configured with pyxsdata metadata."""
    return FieldInfo(
        metadata=metadata,
        default=default,
        default_factory=default_factory,
        **kwargs,
    )
