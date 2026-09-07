from pyxsdata.formats.dataclass.compat import class_types
from pyxsdata.pydantic.compat import Pydantic

class_types.register("pydantic", Pydantic())
