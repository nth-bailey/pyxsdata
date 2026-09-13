# Pydantic v2 Integration

`pyxsdata` natively supports [Pydantic](https://docs.pydantic.dev/) v2 as a first-class
citizen! You can generate Pydantic models directly from XML schemas, WSDLs, and JSON
schemas, and serialize/deserialize them seamlessly.

## Installation

To enable Pydantic support, install `pyxsdata` with the `pydantic` extra:

```console
$ pip install "pyxsdata[cli,pydantic]"
```

## Code Generation

To generate Pydantic models instead of standard standard library dataclasses, specify
`--output pydantic` in the CLI:

```console
$ pyxsdata schema.xsd --output pydantic --package myapp.models
```

Or configure it in `.pyxsdata.xml`:

```xml
<Config xmlns="http://pypi.org/project/pyxsdata">
    <Output format="pydantic">
        <Package>myapp.models</Package>
    </Output>
</Config>
```

### Generated Model Features

- Models inherit from `pydantic.BaseModel`.
- Fields use `pydantic.Field` with validation constraints (e.g. `ge`, `le`, `pattern`,
  `max_length`).
- XML metadata is mapped into field metadata.

## Data Binding

All `pyxsdata` parsers and serializers support Pydantic models. You can either use the
pre-configured shortcuts from `pyxsdata.pydantic.bindings` or specify
`class_type="pydantic"` in `XmlContext`.

### Convenient Binding Shortcuts

`pyxsdata.pydantic.bindings` provides drop-in subclasses with the Pydantic context
automatically configured:

```python
from pyxsdata.pydantic.bindings import (
    CoreXmlParser,
    DictDecoder,
    DictEncoder,
    JsonParser,
    JsonSerializer,
    PycodeSerializer,
    TreeParser,
    UserXmlParser,
    XmlContext,
    XmlParser,
    XmlSerializer,
)

# Parse XML directly into Pydantic models
parser = XmlParser()
order = parser.from_string(xml_content, PurchaseOrder)

# Validate and manipulate with Pydantic
assert isinstance(order, PurchaseOrder)
print(order.model_dump())

# Serialize back to XML
serializer = XmlSerializer()
output_xml = serializer.render(order)
```

### Computed Fields Support (`@computed_field`)

Pydantic v2's `@computed_field` decorator is fully supported. Properties decorated with
`@computed_field` are automatically included during serialization to XML, JSON, and
dictionaries:

```python
from pydantic import BaseModel, computed_field
from pyxsdata.pydantic.bindings import XmlSerializer


class Product(BaseModel):
    unit_price: float
    quantity: int

    @computed_field(alias="TotalPrice")
    @property
    def total(self) -> float:
        return round(self.unit_price * self.quantity, 2)


product = Product(unit_price=19.99, quantity=3)
serializer = XmlSerializer()
print(serializer.render(product))
# <Product>
#   <unit_price>19.99</unit_price>
#   <quantity>3</quantity>
#   <TotalPrice>59.97</TotalPrice>
# </Product>
```

You can also customize the XML field metadata for computed fields via
`json_schema_extra`:

```python
@computed_field(
    json_schema_extra={"metadata": {"type": "Attribute", "name": "sku"}}
)
@property
def item_sku(self) -> str:
    return f"SKU-{self.id}"
```

### High-Performance Native Rust Parsing & Serialization (`CoreXmlParser`, `CoreXmlSerializer`)

When maximum parsing throughput is required, install `pyxsdata[core]` to leverage
`PolyXML` written in Rust. `CoreXmlParser` natively creates Pydantic v2 model instances
at over **310,000 objects/sec** (over 7.6x faster than standard Python parsing):

```python
from pyxsdata.pydantic import CoreXmlParser, CoreXmlSerializer

parser = CoreXmlParser()
order = parser.from_string(xml_content, PurchaseOrder)

serializer = CoreXmlSerializer()
output_xml = serializer.render(order)
```

### Manual Context Configuration

If you prefer using the standard `pyxsdata.formats.dataclass` classes, configure
`XmlContext` with `class_type="pydantic"`:

```python
from pyxsdata.formats.dataclass.context import XmlContext
from pyxsdata.formats.dataclass.parsers import XmlParser
from pyxsdata.formats.dataclass.serializers import XmlSerializer

context = XmlContext(class_type="pydantic")
parser = XmlParser(context=context)
serializer = XmlSerializer(context=context)
```
