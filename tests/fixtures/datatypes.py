from collections import namedtuple
from typing import Any

from pyxsdata.exceptions import ConverterError
from pyxsdata.formats.converter import Converter, converter

Telephone = namedtuple("Telephone", ["country_code", "area_code", "number"])


class PhoneConverter(Converter):
    def deserialize(self, value: Any, **kwargs: Any) -> Any:
        parts = value.split("-")
        if len(parts) == 3:
            return Telephone(*map(int, parts))

        raise ConverterError

    def serialize(self, value: Telephone, **kwargs: Any) -> str:
        return "-".join(map(str, value))


converter.register_converter(Telephone, PhoneConverter())
