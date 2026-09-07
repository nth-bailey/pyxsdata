import os

from click.testing import CliRunner

from pyxsdata.cli import cli
from pyxsdata.utils.testing import load_class
from tests import fixtures_dir, root

os.chdir(root)


def test_books_schema() -> None:
    schema = fixtures_dir.joinpath("books/schema.xsd")
    package = "tests.fixtures.books"
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "generate",
            str(schema),
            "--package",
            package,
            "--structure-style=namespaces",
            "--docstring-style=Google",
        ],
        catch_exceptions=False,
    )

    if result.exception:
        raise result.exception

    clazz = load_class(result.output, "Books")
    assert clazz.Meta.name == "books"
    assert clazz.Meta.namespace == "urn:books"
