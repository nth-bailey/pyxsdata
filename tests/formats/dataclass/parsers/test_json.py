from pyxsdata.formats.dataclass.parsers.json import JsonParser
from pyxsdata.utils.testing import FactoryTestCase
from tests import fixtures_dir
from tests.fixtures.books import Books


class JsonParserTests(FactoryTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.parser = JsonParser()

    def test_parser_entry_points(self) -> None:
        path = fixtures_dir.joinpath("books/books.json")

        books = self.parser.from_path(path)
        self.assertIsInstance(books, Books)

        books = self.parser.from_string(path.read_text(), Books)
        self.assertIsInstance(books, Books)

        books = self.parser.from_bytes(path.read_bytes(), Books)
        self.assertIsInstance(books, Books)

        books = self.parser.parse(str(path), Books)
        self.assertIsInstance(books, Books)
