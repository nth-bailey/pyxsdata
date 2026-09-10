from unittest import TestCase

from pyxsdata.exceptions import XmlContextError
from pyxsdata.formats.dataclass.models.generics import DerivedElement
from pyxsdata.formats.dataclass.parsers.config import ParserConfig
from pyxsdata.formats.dataclass.parsers.nodes import StandardNode
from pyxsdata.models.enums import DataType
from pyxsdata.utils.testing import XmlMetaFactory, XmlVarFactory
from tests.fixtures.artists import Artist


class StandardNodeTests(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.meta = XmlMetaFactory.create(clazz=Artist)
        self.var = XmlVarFactory.create()
        self.config = ParserConfig()

    def test_bind_simple(self) -> None:
        datatype = DataType.INT
        node = StandardNode(
            self.meta, self.var, datatype, {}, self.config, False, False
        )
        objects = []

        self.assertTrue(node.bind("a", "13", None, objects))
        self.assertEqual(("a", 13), objects[-1])

    def test_bind_derived(self) -> None:
        datatype = DataType.INT
        node = StandardNode(
            self.meta,
            self.var,
            datatype,
            {},
            self.config,
            False,
            DerivedElement,
        )
        objects = []

        self.assertTrue(node.bind("a", "13", None, objects))
        self.assertEqual(("a", DerivedElement("a", 13)), objects[-1])

    def test_bind_wrapper_type(self) -> None:
        datatype = DataType.HEX_BINARY
        node = StandardNode(
            self.meta,
            self.var,
            datatype,
            {},
            self.config,
            False,
            DerivedElement,
        )
        objects = []

        self.assertTrue(node.bind("a", "13", None, objects))
        self.assertEqual(
            ("a", DerivedElement(qname="a", value=b"\x13")), objects[-1]
        )

    def test_bind_nillable(self) -> None:
        datatype = DataType.STRING
        node = StandardNode(
            self.meta, self.var, datatype, {}, self.config, True, None
        )
        objects = []

        self.assertTrue(node.bind("a", None, None, objects))
        self.assertEqual(("a", None), objects[-1])

        node.nillable = False
        self.assertTrue(node.bind("a", None, None, objects))
        self.assertEqual(("a", ""), objects[-1])

    def test_child(self) -> None:
        datatype = DataType.STRING
        node = StandardNode(
            self.meta, self.var, datatype, {}, self.config, False, False
        )

        with self.assertRaises(XmlContextError):
            node.child("foo", {}, {}, 0)
