from unittest import TestCase

from pyxsdata.codegen.exceptions import CodegenError
from pyxsdata.models.wsdl import PortType, PortTypeOperation


class PortTypeTests(TestCase):
    def test_find_operating(self) -> None:
        res = PortTypeOperation(name="foo")
        obj = PortType(operations=[res])

        self.assertEqual(res, obj.find_operation("foo"))

        with self.assertRaises(CodegenError):
            obj.find_operation("nope")
