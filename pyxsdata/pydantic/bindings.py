from collections.abc import Callable
from dataclasses import dataclass, field

from pyxsdata.formats.dataclass import context, parsers, serializers
from pyxsdata.pydantic import compat as _compat  # noqa: F401
from pyxsdata.utils.constants import return_input


class XmlContext(context.XmlContext):
    """The models context class for Pydantic.

    The context is responsible to provide binding metadata
    for models and their fields.

    Args:
        element_name_generator: Default element name generator
        attribute_name_generator: Default attribute name generator
        models_package: Restrict auto locate to a specific package

    Attributes:
        cache: Internal cache for binding metadata instances
        xsi_cache: Internal cache for xsi types to class locations
        sys_modules: The number of loaded sys modules
    """

    def __init__(
        self,
        element_name_generator: Callable = return_input,
        attribute_name_generator: Callable = return_input,
        models_package: str | None = None,
    ) -> None:
        """Initialize XmlContext for Pydantic models."""
        super().__init__(
            element_name_generator, attribute_name_generator, "pydantic", models_package
        )


@dataclass
class XmlParser(parsers.XmlParser):
    """Default XML parser for Pydantic models.

    Args:
        config: The parser config instance
        context: The XML context instance
        handler: The XML handler class

    Attributes:
        ns_map: The parsed namespace prefix-URI map
    """

    context: XmlContext = field(default_factory=XmlContext)


@dataclass
class XmlSerializer(serializers.XmlSerializer):
    """XML serializer for Pydantic models.

    Args:
        config: The serializer config instance
        context: The models context instance
        writer: The XML writer class
    """

    context: XmlContext = field(default_factory=XmlContext)


@dataclass
class JsonParser(parsers.JsonParser):
    """JSON parser for Pydantic models.

    Args:
        config: Parser configuration
        context: The models context instance
        load_factory: JSON loader factory
    """

    context: XmlContext = field(default_factory=XmlContext)


@dataclass
class DictDecoder(parsers.DictDecoder):
    """Bind a dictionary or a list of dictionaries to Pydantic models.

    Args:
        config: Parser configuration
        context: The models context instance
    """

    context: XmlContext = field(default_factory=XmlContext)


@dataclass
class DictEncoder(serializers.DictEncoder):
    """Encode Pydantic models to a dictionary.

    Args:
        config: Parser configuration
        context: The models context instance
    """

    context: XmlContext = field(default_factory=XmlContext)


@dataclass
class JsonSerializer(serializers.JsonSerializer):
    """JSON serializer for Pydantic models.

    Args:
        config: The serializer config instance
        context: The models context instance
        dict_factory: Dictionary factory
        dump_factory: JSON dump factory e.g. json.dump
    """

    context: XmlContext = field(default_factory=XmlContext)


@dataclass
class UserXmlParser(parsers.UserXmlParser):
    """XML parser for Pydantic models with hooks to events.

    The event hooks allow custom parsers to inject custom
    logic between the start/end element events.

    Args:
        config: The parser config instance
        context: The XML context instance
        handler: The XML handler class

    Attributes:
        ns_map: The parsed namespace prefix-URI map
        hooks_cache: The hooks cache is used to avoid
            inspecting the class for custom methods
            on duplicate events.
    """

    context: XmlContext = field(default_factory=XmlContext)


@dataclass
class TreeParser(parsers.TreeParser):
    """Bind XML nodes to a tree of AnyElement objects."""

    context: XmlContext = field(default_factory=XmlContext)


@dataclass
class PycodeSerializer(serializers.PycodeSerializer):
    """Python code serializer for Pydantic model instances.

    Generates executable Python code that instantiates the given model.

    Args:
        context: The models context instance
    """

    context: XmlContext = field(default_factory=XmlContext)
