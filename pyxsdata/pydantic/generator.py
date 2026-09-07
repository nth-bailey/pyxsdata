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
        """Return the field definition with any extra metadata."""
        result = super().field_definition(obj, attr, parent_namespace)

        if attr.is_prohibited:
            if attr.is_optional and attr.default is None:
                result = result.replace("init=False", "exclude=True")
            else:
                result = result.replace("init=False", "exclude=True, default=None")
        elif attr.fixed:
            result = result.replace("init=False", "const=True")

        return result

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
