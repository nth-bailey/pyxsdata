from __future__ import annotations

import re
import warnings
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from io import TextIOBase
from pathlib import Path
from re import Pattern
from typing import Any

from pyxsdata import __version__
from pyxsdata.codegen.exceptions import CodegenError, CodegenWarning
from pyxsdata.formats.dataclass.context import XmlContext
from pyxsdata.formats.dataclass.parsers import XmlParser
from pyxsdata.formats.dataclass.parsers.config import ParserConfig
from pyxsdata.formats.dataclass.serializers import XmlSerializer
from pyxsdata.formats.dataclass.serializers.config import SerializerConfig
from pyxsdata.formats.dataclass.serializers.writers import XmlEventWriter
from pyxsdata.models.enums import Namespace
from pyxsdata.utils import objects, text


class StructureStyle(Enum):
    """Output structure style enumeration.

    Attributes:
        FILENAMES: filenames: groups classes by the schema location
        NAMESPACES: namespaces: group classes by the target namespace
        CLUSTERS: clusters: group by strong connected dependencies
        SINGLE_PACKAGE: single-package: group all classes together
        NAMESPACE_CLUSTERS: namespace-clusters: group by strong
            connected dependencies and namespaces
    """

    FILENAMES = "filenames"
    NAMESPACES = "namespaces"
    CLUSTERS = "clusters"
    SINGLE_PACKAGE = "single-package"
    NAMESPACE_CLUSTERS = "namespace-clusters"


class NameCase(Enum):
    """Naming case convention enumeration.

    All schemes are using a processor that splits a string into words
    when it encounters non-alphanumerical characters or when an upper
    case letter follows a lower case letter.

    Attributes:
        ORIGINAL: originalCase
        PASCAL: pascalCase
        CAMEL: camelCase
        SNAKE: snakeCase
        SCREAMING_SNAKE: screamingSnakeCase
        MIXED: mixedCase
        MIXED_SNAKE: mixedSnakeCase
        MIXED_PASCAL: mixedPascalCase
    """

    ORIGINAL = "originalCase"
    PASCAL = "pascalCase"
    CAMEL = "camelCase"
    SNAKE = "snakeCase"
    SCREAMING_SNAKE = "screamingSnakeCase"
    MIXED = "mixedCase"
    MIXED_SNAKE = "mixedSnakeCase"
    MIXED_PASCAL = "mixedPascalCase"

    def __call__(self, string: str, **kwargs: Any) -> str:
        """Apply the callback to the input string."""
        return self.callback(string, **kwargs)

    @property
    def callback(self) -> Callable:
        """Return the actual callable of the scheme."""
        return __name_case_func__[self.value]


__name_case_func__: dict[str, Callable] = {
    "originalCase": text.original_case,
    "pascalCase": text.pascal_case,
    "camelCase": text.camel_case,
    "snakeCase": text.snake_case,
    "screamingSnakeCase": text.screaming_snake_case,
    "mixedCase": text.mixed_case,
    "mixedSnakeCase": text.mixed_snake_case,
    "mixedPascalCase": text.mixed_pascal_case,
}


class DocstringStyle(Enum):
    """Docstring style enumeration.

    Attributes:
        RST: reStructuredText
        NUMPY: NumPy
        GOOGLE: Google
        ACCESSIBLE: Accessible
        BLANK: Blank
    """

    RST = "reStructuredText"
    NUMPY = "NumPy"
    GOOGLE = "Google"
    ACCESSIBLE = "Accessible"
    BLANK = "Blank"


class ObjectType(Enum):
    """Object type enumeration.

    Attributes:
        CLASS: class
        FIELD: field
        MODULE: module
        PACKAGE: package
    """

    CLASS = "class"
    FIELD = "field"
    MODULE = "module"
    PACKAGE = "package"


class ExtensionType(Enum):
    """Extension type enumeration.

    Attributes:
        CLASS: class
        DECORATOR: decorator
    """

    CLASS = "class"
    DECORATOR = "decorator"


@dataclass
class OutputFormat:
    """Output format model representation.

    Args:
        value: Output format name
        repr: Generate __repr__ method
        eq: Generate __eq__ method
        order: Generate __lt__, __le__, __gt__, and __ge__ methods
        unsafe_hash: Generate __hash__ method
        frozen: Enable read only properties
        slots: Enable __slots__
    """

    value: str = field(
        default="dataclasses", metadata={"type": "Text", "cli": "output"}
    )
    repr: bool = field(default=True, metadata={"type": "Attribute"})
    eq: bool = field(default=True, metadata={"type": "Attribute"})
    order: bool = field(default=False, metadata={"type": "Attribute"})
    unsafe_hash: bool = field(default=False, metadata={"type": "Attribute"})
    frozen: bool = field(default=False, metadata={"type": "Attribute"})
    slots: bool = field(default=False, metadata={"type": "Attribute"})

    def __post_init__(self):
        """Post initialization method."""
        self.validate()

    def validate(self) -> None:
        """Validate and reset configuration conflicts."""
        if self.order and not self.eq:
            self.eq = True
            warnings.warn(
                "Enabling eq because order is true",
                CodegenWarning,
            )


@dataclass
class CompoundFields:
    """Compound fields model representation.

    Args:
        enabled: Use compound fields for repeatable elements
        default_name: Default compound field name
        use_substitution_groups: Use substitution groups if they
            exist, instead of element names.
        force_default_name: Always use the default compound field
            name, or try to generate one by the list of element names if
            they are no longer than the max name parts. e.g.
            hat_or_dress_or_something.
        max_name_parts: Maximum number of element names before using
            the default name.
    """

    enabled: bool = field(
        default=False, metadata={"type": "Text", "cli": "compound-fields"}
    )
    default_name: str = field(
        default="choice", metadata={"type": "Attribute", "cli": False}
    )
    use_substitution_groups: bool = field(
        default=False, metadata={"type": "Attribute", "cli": False}
    )
    force_default_name: bool = field(
        default=False, metadata={"type": "Attribute", "cli": False}
    )
    max_name_parts: int = field(default=3, metadata={"type": "Attribute", "cli": False})


@dataclass
class GeneratorOutput:
    """Generator output model representation.

    Args:
        package: Target package
        format: Output format
        structure_style: Output structure style
        docstring_style: Docstring style
        relative_imports: Use relative imports
        compound_fields: Use compound fields for repeatable elements
        wrapper_fields: Generate wrapper fields
        max_line_length: Adjust the maximum line length
        generic_collections: Use generic collections (Iterable, Mapping)
        unnest_classes: Move inner classes to upper level
        ignore_patterns: Ignore pattern restrictions
        include_header: Include a header with codegen information in the output
        str_enums: Generate StrEnum for string enumerations
    """

    package: str = field(default="generated", metadata={"type": "Element"})
    format: OutputFormat = field(
        default_factory=OutputFormat, metadata={"type": "Element"}
    )
    structure_style: StructureStyle = field(
        default=StructureStyle.FILENAMES,
        metadata={"type": "Element", "name": "Structure"},
    )
    docstring_style: DocstringStyle = field(
        default=DocstringStyle.RST, metadata={"type": "Element"}
    )
    relative_imports: bool = field(default=False, metadata={"type": "Element"})
    compound_fields: CompoundFields = field(
        default_factory=CompoundFields, metadata={"type": "Element"}
    )
    wrapper_fields: bool = field(default=False, metadata={"type": "Element"})
    max_line_length: int = field(default=79, metadata={"type": "Attribute"})
    generic_collections: bool = field(default=False, metadata={"type": "Attribute"})
    unnest_classes: bool = field(default=False, metadata={"type": "Element"})
    ignore_patterns: bool = field(default=False, metadata={"type": "Element"})
    include_header: bool = field(default=False, metadata={"type": "Element"})
    str_enums: bool = field(
        default=False, metadata={"type": "Attribute", "cli": "str-enums"}
    )

    def __post_init__(self):
        """Post initialization method."""
        self.validate()

    def validate(self) -> None:
        """Reset configuration conflicts."""
        if self.generic_collections and self.format.frozen:
            self.generic_collections = False
            warnings.warn(
                "Generic Collections, requires frozen=False, reverting...",
                CodegenWarning,
            )

    def update(self, **kwargs: Any) -> None:
        """Update instance attributes recursively."""
        objects.update(self, **kwargs)
        self.format.validate()


@dataclass
class NameConvention:
    """Name convention model representation.

    Args:
        case: Naming scheme, e.g. camelCase, snakeCase
        safe_prefix: A prefix to be prepended into names that match
            one of the reserved words.
    """

    case: NameCase = field(metadata={"type": "Attribute"})
    safe_prefix: str = field(metadata={"type": "Attribute"})


@dataclass
class GeneratorConventions:
    """Generator naming conventions model representation.

    Args:
        class_name: Class naming conventions.
        field_name: Field naming conventions.
        module_name: Module naming conventions.
        package_name: Package naming conventions.
    """

    class_name: NameConvention = field(
        default_factory=lambda: NameConvention(NameCase.PASCAL, "type"),
        metadata={"type": "Element"},
    )
    field_name: NameConvention = field(
        default_factory=lambda: NameConvention(NameCase.SNAKE, "value"),
        metadata={"type": "Element"},
    )
    constant_name: NameConvention = field(
        default_factory=lambda: NameConvention(NameCase.SCREAMING_SNAKE, "value"),
        metadata={"type": "Element"},
    )
    module_name: NameConvention = field(
        default_factory=lambda: NameConvention(NameCase.SNAKE, "mod"),
        metadata={"type": "Element"},
    )
    package_name: NameConvention = field(
        default_factory=lambda: NameConvention(NameCase.SNAKE, "pkg"),
        metadata={"type": "Element"},
    )


@dataclass
class GeneratorAlias:
    """Generator alias model representation.

    Define an alias for a module, package, class and field Alias definition
    model.

    Each alias has a source attribute that refers to the original name
    in the schema definition and the target attribute for output name.
    For package and module aliases the source refers to the schema
    filename or target namespace depending on the selected output
    structure.

    Args:
        source: The source name from schema definition
        target: The target name of the object.
    """

    source: str = field(metadata={"type": "Attribute", "required": True})
    target: str = field(metadata={"type": "Attribute", "required": True})


@dataclass
class GeneratorAliases:
    """Generator aliases model representation.

    Generator aliases for classes, fields, packages and modules
    that bypass the global naming conventions. The aliases
    are not validated as valid python identifiers.

    Args:
        class_name: A list of class name aliases
        field_name: A list of field name aliases
        package_name: A list of package name aliases
        module_name: A list of module name aliases
    """

    class_name: list[GeneratorAlias] = field(
        default_factory=list, metadata={"type": "Element"}
    )
    field_name: list[GeneratorAlias] = field(
        default_factory=list, metadata={"type": "Element"}
    )
    package_name: list[GeneratorAlias] = field(
        default_factory=list, metadata={"type": "Element"}
    )
    module_name: list[GeneratorAlias] = field(
        default_factory=list, metadata={"type": "Element"}
    )


@dataclass
class GeneratorSubstitution:
    """Generator substitution model representation.

    Search and replace substitutions based on `re.sub`.

    Args:
        type: The target object type
        search: The search string or a pattern object
        replace: The replacement string or pattern object
    """

    type: ObjectType = field(metadata={"type": "Attribute", "required": True})
    search: str = field(metadata={"type": "Attribute", "required": True})
    replace: str = field(metadata={"type": "Attribute", "required": True})


@dataclass
class GeneratorExtension:
    """Generator extension model representation.

    Add decorators or base classes on the generated classes
    that match the class name pattern.

    Args:
        type: The extension type
        class_name: The class name or a pattern to apply the extension
        import_string: The import string of the extension type
        prepend: Prepend or append decorator or base class
        apply_if_derived: Apply or skip if the class is already a subclass
        parent_path: Optional pattern against the fully-qualified parent element name

    Attributes:
        module_path: The module path of the base class or the annotation
        func_name: The annotation or base class name
        pattern: The compiled search class name pattern
        parent_pattern: The compiled search parent pattern or None
    """

    type: ExtensionType = field(metadata={"type": "Attribute", "required": True})
    class_name: str = field(
        metadata={"type": "Attribute", "required": True, "name": "class"}
    )
    import_string: str = field(
        metadata={"type": "Attribute", "required": True, "name": "import"}
    )
    prepend: bool = field(default=False, metadata={"type": "Attribute"})
    apply_if_derived: bool = field(
        default=False, metadata={"type": "Attribute", "name": "applyIfDerived"}
    )

    module_path: str = field(
        init=False,
        metadata={"type": "Ignore"},
    )
    func_name: str = field(
        init=False,
        metadata={"type": "Ignore"},
    )
    pattern: Pattern = field(
        init=False,
        metadata={"type": "Ignore"},
    )

    parent_path: str | None = field(
        default=None,
        metadata={"type": "Attribute", "required": False, "name": "module"},
    )
    parent_pattern: Pattern | None = field(
        init=False,
        metadata={"type": "Ignore"},
    )

    def __post_init__(self):
        """Post initialization method.

        Set the module, func_name and pattern instance attributes.

        Raises:
            GeneratorConfigError: If the pattern can not be compiled.
        """
        try:
            self.module_path, self.func_name = self.import_string.rsplit(".", 1)
        except (ValueError, AttributeError):
            raise CodegenError(
                "Invalid extension import string", value=self.import_string
            )

        try:
            self.pattern = re.compile(self.class_name)
        except re.error:
            raise CodegenError(
                "Failed to compile extension pattern", pattern=self.class_name
            )

        self.parent_pattern = None
        if self.parent_path:
            try:
                self.parent_pattern = re.compile(self.parent_path)
            except re.error:
                raise CodegenError(
                    "Failed to compile extension parent pattern",
                    pattern=self.parent_path,
                )


@dataclass
class GeneratorSubstitutions:
    """Generator substitutions model representation.

    Generator search and replace substitutions for classes, fields, packages
    and modules names. The process runs before and after the default naming
    conventions.

    Args:
        substitution: The list of substitution instances
    """

    substitution: list[GeneratorSubstitution] = field(
        default_factory=list, metadata={"type": "Element"}
    )


@dataclass
class GeneratorExtensions:
    """Generator extensions model representation.

    Generator extensions for classes. The process runs after the
    default naming conventions. The generator doesn't validate
    imports!

    Args:
        extension: The list of extension instances
    """

    extension: list[GeneratorExtension] = field(
        default_factory=list, metadata={"type": "Element"}
    )


@dataclass
class GeneratorConfig:
    """Generator configuration model representation.

    Args:
        output: Output options
        conventions: Generator conventions
        substitutions: Search and replace substitutions for
            classes, fields, packages and modules names.
        extensions: Generator custom base classes and decorators for classes.

    Attributes:
        version: The xsdata version number the config was created/updated
    """

    class Meta:
        """Metadata options."""

        name = "Config"
        namespace = "http://pypi.org/project/xsdata"

    version: str = field(default=__version__, metadata={"type": "Attribute"})
    output: GeneratorOutput = field(
        default_factory=GeneratorOutput, metadata={"type": "Element"}
    )
    conventions: GeneratorConventions = field(
        default_factory=GeneratorConventions, metadata={"type": "Element"}
    )
    substitutions: GeneratorSubstitutions = field(
        default_factory=GeneratorSubstitutions, metadata={"type": "Element"}
    )
    extensions: GeneratorExtensions = field(
        default_factory=GeneratorExtensions, metadata={"type": "Element"}
    )

    @classmethod
    def create(cls) -> GeneratorConfig:
        """Initialize with default substitutions for common namespaces."""
        obj = cls()

        for ns in Namespace:
            obj.substitutions.substitution.append(
                GeneratorSubstitution(
                    type=ObjectType.PACKAGE, search=ns.uri, replace=ns.prefix
                )
            )

        obj.substitutions.substitution.append(
            GeneratorSubstitution(
                type=ObjectType.CLASS, search="(.*)Class$", replace="\\1Type"
            )
        )

        return obj

    @classmethod
    def read(cls, path: Path) -> GeneratorConfig:
        """Load configuration from a file path."""
        if not path.exists():
            return cls()

        ctx = XmlContext(
            element_name_generator=text.pascal_case,
            attribute_name_generator=text.camel_case,
        )
        parser = XmlParser(
            context=ctx,
            config=ParserConfig(
                fail_on_unknown_properties=False,
                fail_on_converter_warnings=True,
            ),
        )
        cfg = parser.from_path(path, cls)
        cfg.version = __version__
        return cfg

    @classmethod
    def write(cls, output: TextIOBase, obj: GeneratorConfig):
        """Write the configuration to the output stream as XML."""
        ctx = XmlContext(
            element_name_generator=text.pascal_case,
            attribute_name_generator=text.camel_case,
        )
        config = SerializerConfig(indent="  ")
        serializer = XmlSerializer(context=ctx, config=config, writer=XmlEventWriter)
        serializer.write(output, obj, ns_map={None: "http://pypi.org/project/xsdata"})
