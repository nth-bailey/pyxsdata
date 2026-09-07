from unittest import mock

from pyxsdata.codegen.handlers import RenameDuplicateAttributes
from pyxsdata.codegen.utils import ClassUtils
from pyxsdata.utils.testing import ClassFactory, FactoryTestCase


class RenameDuplicateAttributesTests(FactoryTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.processor = RenameDuplicateAttributes()

    @mock.patch.object(ClassUtils, "rename_duplicate_attributes")
    def test_process(self, mock_rename_duplicate_attributes) -> None:
        target = ClassFactory.create()
        self.processor.process(target)

        mock_rename_duplicate_attributes.assert_called_once_with(target)
