import os

from click.testing import CliRunner

from pyxsdata.cli import cli
from pyxsdata.utils.testing import load_class
from tests import fixtures_dir, root
from tests.conftest import validate_bindings

os.chdir(root)


def test_primer_schema() -> None:
    schema = fixtures_dir.joinpath("primer/order.xsd")
    package = "tests.fixtures.primer"
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["generate", str(schema), "--package", package, "--docstring-style", "NumPy"],
    )

    if result.exception:
        raise result.exception

    clazz = load_class(result.output, "PurchaseOrder")
    assert clazz.Meta.name == "purchaseOrder"

    validate_bindings(schema, clazz)
