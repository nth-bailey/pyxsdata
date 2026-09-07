from pathlib import Path

from click.testing import CliRunner

from pyxsdata.cli import cli
from pyxsdata.models.config import GeneratorConfig
from pyxsdata.pydantic.generator import PydanticGenerator
from pyxsdata.utils.testing import FactoryTestCase


class PydanticGeneratorTests(FactoryTestCase):
    def setUp(self) -> None:
        super().setUp()
        config = GeneratorConfig()
        self.generator = PydanticGenerator(config)

    def test_complete(self) -> None:
        runner = CliRunner()
        fixtures_dir = Path(__file__).parent.joinpath("fixtures")
        schema = fixtures_dir.joinpath("schemas/po.xsd")
        config_file = fixtures_dir.joinpath("pydantic.conf.xml")

        result = runner.invoke(
            cli,
            [
                "generate",
                str(schema),
                "--package",
                "tests.pydantic.fixtures.po.models",
                "--structure-style=single-package",
                "--output",
                "pydantic",
                "--config",
                str(config_file),
            ],
            catch_exceptions=True,
        )

        self.assertIsNone(result.exception)

    def test_field_definition_prohibited_and_fixed(self) -> None:
        from pyxsdata.codegen.models import AttrType
        from pyxsdata.pydantic.generator import PydanticFilters
        from pyxsdata.utils.testing import AttrFactory, ClassFactory

        filters = PydanticFilters(GeneratorConfig())
        obj = ClassFactory.create()
        attr_prohibited = AttrFactory.create(
            name="prohibited_attr",
            types=[AttrType(qname="str")],
        )
        attr_prohibited.restrictions.max_occurs = 0

        attr_fixed = AttrFactory.create(
            name="fixed_attr",
            types=[AttrType(qname="str")],
            fixed=True,
        )

        res_prohibited = filters.field_definition(obj, attr_prohibited, None)
        self.assertIn("exclude=True", res_prohibited)
        self.assertIn("default=None", res_prohibited)

        attr_prohibited_optional = AttrFactory.create(
            name="prohibited_optional_attr",
            types=[AttrType(qname="str")],
        )
        attr_prohibited_optional.restrictions.min_occurs = 0
        attr_prohibited_optional.restrictions.max_occurs = 0
        res_prohibited_optional = filters.field_definition(
            obj, attr_prohibited_optional, None
        )
        self.assertIn("exclude=True", res_prohibited_optional)
        self.assertEqual(res_prohibited_optional.count("default="), 1)

        res_fixed = filters.field_definition(obj, attr_fixed, None)
        self.assertIn("frozen=True", res_fixed)

        attr_restricted = AttrFactory.create(
            name="quantity",
            types=[AttrType(qname="int")],
        )
        attr_restricted.restrictions.min_inclusive = "5"
        attr_restricted.restrictions.max_exclusive = "100"
        res_restricted = filters.field_definition(obj, attr_restricted, None)
        self.assertIn("ge=5", res_restricted)
        self.assertIn("lt=100", res_restricted)

        attr_float = AttrFactory.create(
            name="price",
            types=[AttrType(qname="float")],
        )
        attr_float.restrictions.min_inclusive = "1.5"
        res_float = filters.field_definition(obj, attr_float, None)
        self.assertIn("ge=1.5", res_float)

        attr_unparsed = AttrFactory.create(
            name="custom",
            types=[AttrType(qname="str")],
        )
        attr_unparsed.restrictions.min_inclusive = "unparsed_val"
        res_unparsed = filters.field_definition(obj, attr_unparsed, None)
        self.assertIn('ge="unparsed_val"', res_unparsed)

    def test_generated_models_validation(self) -> None:
        from pydantic import ValidationError

        from tests.pydantic.fixtures.po.models import Items, Usaddress

        # Valid model instantiation
        item = Items.Item(
            quantity=50,
            part_num="123-AB",
            product_name="Sample",
            usprice=10,
        )
        self.assertEqual(item.quantity, 50)
        self.assertEqual(item.part_num, "123-AB")

        # Quantity constraint: lt=100
        with self.assertRaises(ValidationError) as ctx:
            Items.Item(
                quantity=150,
                part_num="123-AB",
                product_name="Sample",
                usprice=10,
            )
        self.assertIn("less_than", str(ctx.exception))

        # Pattern constraint: pattern=r"\d{3}-[A-Z]{2}"
        with self.assertRaises(ValidationError) as ctx:
            Items.Item(
                quantity=50,
                part_num="INVALID",
                product_name="Sample",
                usprice=10,
            )
        self.assertIn("string_pattern_mismatch", str(ctx.exception))

        # Frozen constraint on country="US"
        addr = Usaddress(
            name="Bob",
            street="123 Main",
            city="Town",
            state="ST",
            zip=12345,
        )
        with self.assertRaises(ValidationError) as ctx:
            addr.country = "CA"
        self.assertIn("frozen_field", str(ctx.exception))
