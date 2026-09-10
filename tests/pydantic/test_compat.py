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

    def test_model_json_schema_with_xml_types(self) -> None:
        from xml.etree.ElementTree import QName

        from pydantic import BaseModel

        from pyxsdata.models.datatype import (
            XmlDate,
            XmlDateTime,
            XmlDuration,
            XmlPeriod,
            XmlTime,
        )

        class XmlModel(BaseModel):
            date: XmlDate | None = None
            datetime: XmlDateTime | None = None
            time: XmlTime | None = None
            duration: XmlDuration | None = None
            period: XmlPeriod | None = None
            qname: QName | None = None

        schema = XmlModel.model_json_schema()
        self.assertEqual(schema["type"], "object")
        properties = schema["properties"]
        for field_name in (
            "date",
            "datetime",
            "time",
            "duration",
            "period",
            "qname",
        ):
            prop = properties[field_name]
            types = [item.get("type") for item in prop.get("anyOf", [prop])]
            self.assertIn("string", types)

    def test_get_fields_on_instance(self) -> None:
        from pydantic import BaseModel

        from pyxsdata.pydantic.fields import field

        class SampleModel(BaseModel):
            name: str = field(metadata={"type": "Element"}, default="test")
            age: int = 42

        instance = SampleModel()
        class_fields = list(self.class_type.get_fields(SampleModel))
        instance_fields = list(self.class_type.get_fields(instance))

        self.assertEqual(len(class_fields), 2)
        self.assertEqual([f.name for f in class_fields], ["name", "age"])
        self.assertEqual(
            [f.name for f in instance_fields], [f.name for f in class_fields]
        )
        self.assertEqual(instance_fields[0].metadata["type"], "Element")

    def test_field_function_helpers(self) -> None:
        from pyxsdata.pydantic.fields import FieldInfo, field

        f1 = field(metadata={"type": "Element"}, default="hello")
        self.assertIsInstance(f1, FieldInfo)
        self.assertEqual(f1.default, "hello")
        self.assertEqual(f1.xsdata_metadata, {"type": "Element"})

        f2 = field(default_factory=list)
        self.assertIsInstance(f2, FieldInfo)
        self.assertEqual(f2.default_factory, list)

        f3 = field()
        self.assertIsInstance(f3, FieldInfo)
