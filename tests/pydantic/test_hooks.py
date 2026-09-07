from unittest import TestCase

from pyxsdata.codegen.writer import CodeWriter
from pyxsdata.formats.dataclass.compat import class_types
from pyxsdata.pydantic.compat import Pydantic
from pyxsdata.pydantic.generator import PydanticGenerator
from pyxsdata.pydantic.hooks import class_type, cli


class PydanticHooksTests(TestCase):
    def test_class_type_hook(self) -> None:
        self.assertIsNotNone(class_type)
        self.assertIsInstance(class_types.get_type("pydantic"), Pydantic)

    def test_cli_hook(self) -> None:
        self.assertIsNotNone(cli)
        self.assertIs(CodeWriter.generators["pydantic"], PydanticGenerator)

    def test_pydantic_module_getattr(self) -> None:
        import pyxsdata.pydantic as pydantic_mod

        self.assertIsNotNone(pydantic_mod.XmlParser)
        self.assertIsNotNone(pydantic_mod.field)
        with self.assertRaises(AttributeError):
            _ = pydantic_mod.non_existent_attribute
