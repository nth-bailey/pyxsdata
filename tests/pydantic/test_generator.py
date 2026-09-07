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
        self.assertIn("exclude=True, default=None", res_prohibited)

        res_fixed = filters.field_definition(obj, attr_fixed, None)
        self.assertIn("const=True", res_fixed)
