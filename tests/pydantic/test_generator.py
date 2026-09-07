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
