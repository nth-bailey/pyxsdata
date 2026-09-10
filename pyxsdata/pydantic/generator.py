import contextlib
from typing import Any

from pyxsdata.codegen.models import Attr, Class
from pyxsdata.formats.dataclass.filters import Filters
from pyxsdata.formats.dataclass.generator import DataclassGenerator
from pyxsdata.models.config import GeneratorConfig
from pyxsdata.utils.text import stop_words

stop_words.update(["validate"])


class PydanticGenerator(DataclassGenerator):
    """Python Pydantic models code generator."""

    @classmethod
    def init_filters(cls, config: GeneratorConfig) -> Filters:
        """Initialize filters for Pydantic code generation."""
        return PydanticFilters(config)


class PydanticFilters(Filters):
    """Template filters for Pydantic model generation."""

    def __init__(self, config: GeneratorConfig):
        """Initialize PydanticFilters."""
        super().__init__(config)
        self.default_class_annotation = None

    def post_meta_hook(self, obj: Class) -> str | None:
        """Add model_config to generated class."""
        return "model_config = ConfigDict(defer_build=True)"

    def class_bases(self, obj: Class, class_name: str) -> list[str]:
        """Return base classes for the generated class."""
        result = super().class_bases(obj, class_name)

        if not obj.extensions:
            result.insert(0, "BaseModel")
        return result

    def field_definition(
        self,
        obj: Class,
        attr: Attr,
        parent_namespace: str | None,
    ) -> str:
        """Return the field definition with Pydantic kwargs and extra metadata."""
        ns_map = obj.ns_map
        default_value = self.field_default_value(attr, ns_map)
        metadata = self.field_metadata(obj, attr, parent_namespace)

        kwargs: dict[str, Any] = {}

        if attr.is_prohibited:
            kwargs["exclude"] = True
            kwargs["default"] = None
        elif attr.fixed:
            kwargs["frozen"] = True
            if default_value is not False:
                kwargs["default"] = default_value
        elif default_value is not False:
            key = "default_factory" if attr.is_factory else "default"
            kwargs[key] = default_value

        for meta_key, pydantic_key in (
            ("min_inclusive", "ge"),
            ("max_inclusive", "le"),
            ("min_exclusive", "gt"),
            ("max_exclusive", "lt"),
            ("min_length", "min_length"),
            ("max_length", "max_length"),
            ("pattern", "pattern"),
        ):
            if meta_key in metadata:
                val = metadata[meta_key]
                if pydantic_key in (
                    "ge",
                    "le",
                    "gt",
                    "lt",
                    "min_length",
                    "max_length",
                ):
                    with contextlib.suppress(ValueError, TypeError):
                        val = int(val)
                    if isinstance(val, str):
                        with contextlib.suppress(ValueError, TypeError):
                            val = float(val)
                kwargs[pydantic_key] = val

        if metadata:
            kwargs["metadata"] = metadata

        return f"field({self.format_arguments(kwargs, 4)})"

    @classmethod
    def build_import_patterns(cls) -> dict[str, dict]:
        """Build import patterns for Pydantic templates."""
        patterns = super().build_import_patterns()
        patterns.update(
            {
                "dataclasses": {},
                "pyxsdata.pydantic.fields": {"field": [" = field("]},
                "pydantic": {
                    "BaseModel": ["(BaseModel"],
                    "Field": [" Field("],
                    "ConfigDict": ["model_config = ConfigDict("],
                },
            }
        )

        return {key: patterns[key] for key in sorted(patterns)}
