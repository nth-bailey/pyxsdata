from pyxsdata.codegen.mixins import HandlerInterface
from pyxsdata.codegen.models import Class
from pyxsdata.codegen.utils import ClassUtils


class RenameDuplicateAttributes(HandlerInterface):
    """Resolve attr name conflicts defined in the class."""

    __slots__ = ()

    def process(self, target: Class) -> None:
        """Detect and resolve naming conflicts.

        Args:
            target: The target class instance
        """
        ClassUtils.rename_duplicate_attributes(target)
