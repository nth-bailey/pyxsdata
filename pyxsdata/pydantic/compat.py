from collections.abc import Callable, Iterator
from dataclasses import MISSING, dataclass
from types import MappingProxyType
from typing import Any, TypeVar
from xml.etree.ElementTree import QName

from pydantic import BaseModel
from pydantic_core import PydanticUndefined, core_schema

from pyxsdata.formats.converter import converter
from pyxsdata.formats.dataclass.compat import Dataclasses, class_types
from pyxsdata.formats.dataclass.models.elements import XmlType
from pyxsdata.models.datatype import (
    XmlDate,
    XmlDateTime,
    XmlDuration,
    XmlPeriod,
    XmlTime,
)
from pyxsdata.pydantic.fields import field

T = TypeVar("T", bound=object)
EMPTY_DICT: dict = {}


@dataclass(slots=True)
class FieldInfo:
    """Class field info wrapper for Pydantic models."""

    name: str
    init: bool
    metadata: MappingProxyType[Any, Any]
    default: Any
    default_factory: Any


class Config:
    """Configuration wrapper for Pydantic models."""

    arbitrary_types_allowed = True


class AnyElement(BaseModel):
    """Generic model to bind XML document data to wildcard fields.

    Args:
        qname: The element's qualified name
        text: The element's text content
        tail: The element's tail content
        children: The element's list of child elements.
        attributes: The element's key-value attribute mappings.
    """

    qname: str | None = field(default=None)
    text: str | None = field(default=None)
    tail: str | None = field(default=None)
    children: list[object] = field(
        default_factory=list, metadata={"type": XmlType.WILDCARD}
    )
    attributes: dict[str, str] = field(
        default_factory=dict, metadata={"type": XmlType.ATTRIBUTES}
    )


class DerivedElement[T](BaseModel):
    """Generic model wrapper for type substituted elements.

    Example: eg. <b xsi:type="a">...</b>

    Args:
        qname: The element's qualified name
        value: The wrapped value
        type: The real xsi:type
    """

    qname: str
    value: T
    type: str | None = None


class Pydantic(Dataclasses):
    """Pydantic class type handler for data binding."""

    @property
    def any_element(self) -> type:
        """Return the generic AnyElement class."""
        return AnyElement

    @property
    def derived_element(self) -> type:
        """Return the generic DerivedElement class."""
        return DerivedElement

    def is_model(self, obj: Any) -> bool:
        """Return whether the given value is a Pydantic model."""
        clazz = obj if isinstance(obj, type) else type(obj)
        return issubclass(clazz, BaseModel)

    def get_fields(self, obj: Any) -> Iterator[FieldInfo]:
        """Yield field information for a Pydantic model in declaration order."""
        for name, info in obj.model_fields.items():
            raw_meta = getattr(info, "xsdata_metadata", None) or EMPTY_DICT
            metadata = MappingProxyType(raw_meta)

            yield FieldInfo(
                name=name,
                init=info.init_var is not False,
                metadata=metadata,
                default=info.default
                if info.default is not PydanticUndefined
                else MISSING,
                default_factory=info.default_factory
                if info.default_factory
                else MISSING,
            )


class_types.register("pydantic", Pydantic())


def set_validator(data_type: Any) -> None:
    """Configure custom pydantic core schema validator for the given data type."""

    def validator(
        cls: Any,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        conv = converter.type_converter(data_type)
        return core_schema.json_or_python_schema(
            json_schema=core_schema.no_info_plain_validator_function(conv.deserialize),
            python_schema=core_schema.is_instance_schema(data_type),
            serialization=core_schema.plain_serializer_function_ser_schema(
                conv.serialize
            ),
        )

    setattr(data_type, "__get_pydantic_core_schema__", classmethod(validator))  # noqa


types = [XmlDate, XmlDateTime, XmlTime, XmlDuration, XmlPeriod, QName]
for tp in types:
    set_validator(tp)
