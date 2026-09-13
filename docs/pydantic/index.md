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

## AI & LLM Workflows: Token Pruning & Sub-Model Projections

Enterprise XML documents and schemas (such as ISO 20022, UBL, HL7, and FIX) can contain
hundreds of deeply nested classes, optional extensions, and namespace noise. Passing
them raw to Large Language Models (OpenAI, Anthropic, Google Gemini, LangChain,
Instructor) quickly blows past token budgets and JSON schema validation limits.

`pyxsdata.pydantic` provides two powerful, dedicated utilities to eliminate this
friction:

### 1. `prune_dump`: Token-Efficient Prompt Ingestion

Before inserting an XML-derived Pydantic model instance into an LLM prompt, use
`prune_dump` to strip namespace noise, empty structures, and unwanted fields with glob
dot-paths:

```python
from pyxsdata.pydantic import XmlParser, prune_dump

# Parse complex 5,000-line enterprise XML
order = XmlParser().from_string(xml_text, EnterprisePurchaseOrder)

# Prune down to only what the prompt needs:
prompt_data = prune_dump(
    order,
    # Retain specific branches or leaf fields with glob dot-paths:
    include=["id", "order_date", "customer.name", "items.*.sku", "items.*.price"],
    # Or exclude heavy internal structures anywhere in the tree:
    exclude=["*.signature", "*.audit_trail"],
    # Exclude entire XML namespaces:
    exclude_namespaces=["http://www.w3.org/2000/09/xmldsig#"],
    # Automatically drop unpopulated data:
    exclude_none=True,   # Drops None values
    exclude_empty=True,  # Drops empty lists [] and dicts {}
    # Output key style:
    key_style="python",  # Clean snake_case keys (default)
)
```

### 2. `project_model`: Lean LLM Structured Outputs

When requesting structured data from an LLM (`response_format` in OpenAI or Tool Calling
in Anthropic/Gemini), sending a 500-field schema causes hallucination, token bloat, or
schema length errors.

`project_model` creates a real, lightweight Pydantic v2 sub-model that preserves all
field validation constraints (`ge`, `le`, `pattern`, `min_length`, etc.) while exposing
only the requested fields in the JSON schema:

```python
from openai import OpenAI
from pyxsdata.pydantic import XmlSerializer, project_model

client = OpenAI()

# 1. Dynamically create a lean sub-model with only the fields to extract:
LLMOrder = project_model(
    EnterprisePurchaseOrder,
    include={"id", "order_date", "customer.name", "items.sku", "items.quantity"},
)

# 2. Pass directly to OpenAI Structured Outputs:
completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Extract purchase order from email..."}],
    response_format=LLMOrder,
)
lean_instance: LLMOrder = completion.choices[0].message.parsed

# 3. Re-hydrate back into the full enterprise model and serialize to valid XML!
full_order = EnterprisePurchaseOrder.model_validate(lean_instance.model_dump())
xml_output = XmlSerializer().render(full_order)
```
