from unittest import TestCase

from pyxsdata.formats.dataclass.compat import class_types
from pyxsdata.pydantic.compat import AnyElement, DerivedElement, Pydantic


class PydanticTests(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.class_type = class_types.get_type("pydantic")

    def test_class_type(self) -> None:
        self.assertIsInstance(self.class_type, Pydantic)

    def test_property_any_element(self) -> None:
        self.assertIs(self.class_type.any_element, AnyElement)

    def test_property_derived_element(self) -> None:
        self.assertIs(self.class_type.derived_element, DerivedElement)
