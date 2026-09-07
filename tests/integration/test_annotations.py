import os

import pytest
from click.testing import CliRunner

from pyxsdata.cli import cli
from pyxsdata.formats.dataclass.context import XmlContext
from pyxsdata.formats.dataclass.parsers.xml import XmlParser
from pyxsdata.utils.testing import load_class
from tests import fixtures_dir, root

os.chdir(root)


def test_annotations() -> None:
    filepath = fixtures_dir.joinpath("annotations")
    schema = filepath.joinpath("model.xsd")
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["generate", str(schema), f"--config={filepath.joinpath('pyxsdata.xml')!s}"],
    )

    if result.exception:
        raise result.exception

    try:
        Measurement = load_class(result.output, "Measurement")
        unit = load_class(result.output, "unit")
    except Exception:
        pytest.fail("Could not load class with member having the same name as type")

    filename = str(filepath.joinpath("sample.xml"))
    parser = XmlParser(context=XmlContext())
    measurement = parser.parse(filename, Measurement)
    assert measurement.value == 2.0
    assert measurement.unit == unit.KG
