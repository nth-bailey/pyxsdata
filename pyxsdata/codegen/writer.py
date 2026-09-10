from __future__ import annotations

from typing import ClassVar

from pyxsdata.codegen.exceptions import CodegenError
from pyxsdata.codegen.models import Class
from pyxsdata.formats.dataclass.generator import DataclassGenerator
from pyxsdata.formats.mixins import AbstractGenerator
from pyxsdata.logger import logger
from pyxsdata.models.config import GeneratorConfig


class CodeWriter:
    """Code writer class.

    Args:
        generator: The code generator instance

    Attributes:
        generators: A map of registered code generators
    """

    __slots__ = "generator"

    generators: ClassVar[dict[str, type[AbstractGenerator]]] = {
        "dataclasses": DataclassGenerator,
    }

    def __init__(self, generator: AbstractGenerator):
        """Initialize CodeWriter."""
        self.generator = generator

    def write(self, classes: list[Class]) -> None:
        """Write the classes to the designated modules.

        The classes may be written in the same module or
        different ones, the entrypoint must create the
        directory structure write the file outputs.

        Args:
            classes: A list of class instances
        """
        self.generator.normalize_packages(classes)
        header = self.generator.render_header()

        for result in self.generator.render(classes):
            if result.source.strip():
                logger.info("Generating package: %s", result.title)
                src_code = header + result.source
                result.path.parent.mkdir(parents=True, exist_ok=True)
                result.path.write_text(src_code, encoding="utf-8")

    @classmethod
    def from_config(cls, config: GeneratorConfig) -> CodeWriter:
        """Instance the code writer from the generator configuration instance.

        Validates that the output format is registered as a generator.

        Args:
            config: The generator configuration instance

        Returns:
            A new code writer instance.
        """
        if config.output.format.value not in cls.generators:
            raise CodegenError(
                "Unknown output format", format=config.output.format.value
            )

        generator_class = cls.generators[config.output.format.value]
        return cls(generator=generator_class(config))

    @classmethod
    def register_generator(cls, name: str, clazz: type[AbstractGenerator]):
        """Register a generator by name.

        Args:
            name: The generator name
            clazz: The generator class
        """
        cls.generators[name] = clazz

    @classmethod
    def unregister_generator(cls, name: str):
        """Remove a generator by name.

        Args:
            name: The generator name
        """
        cls.generators.pop(name)


try:
    from pyxsdata.pydantic.generator import PydanticGenerator

    CodeWriter.register_generator("pydantic", PydanticGenerator)
except ImportError:  # pragma: no cover
    pass
