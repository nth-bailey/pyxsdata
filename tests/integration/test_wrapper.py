import os

from click.testing import CliRunner

from pyxsdata.cli import cli
from pyxsdata.utils.testing import load_class
from tests import fixtures_dir, root
from tests.conftest import validate_bindings

os.chdir(root)


def test_xml_documents() -> None:
    schema = fixtures_dir.joinpath("wrapper/schema.xsd")
    package = "tests.fixtures.wrapper.models"
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "generate",
            str(schema),
            "-p",
            package,
            "-ss",
            "single-package",
            "--wrapper-fields",
            "--compound-fields",
        ],
    )

    if result.exception:
        raise result.exception

    clazz = load_class(result.output, "Wrapper")
    validate_bindings(schema, clazz)
