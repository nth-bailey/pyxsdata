# Frequently Asked Questions (FAQ)

---

### How does `pyxsdata` differ from legacy `xsdata`?

`pyxsdata` is an actively maintained, modernized successor designed exclusively for **Python 3.12+**. Key differences include:

1. **Native Pydantic v2 Support**: `xsdata-pydantic` has been consolidated directly into `pyxsdata.pydantic`. You do not need to install or configure external plugins.
2. **Strict CLI**: The CLI command is strictly `pyxsdata` with zero legacy shims.
3. **Pugixml Streaming Parser**: Built-in `PugixmlEventHandler` powered by `pygixml` provides ultra-fast C++ pull-parsing.
4. **Python 3.12+ Standards**: All generated dataclasses use `kw_only=True` by default, full type annotations use `X | Y` union syntax, and the codebase is statically checked with Astral `ty`.

---

### Should I choose standard Dataclasses or Pydantic v2?

Both are first-class citizens in `pyxsdata`!

- **Choose Standard Dataclasses** if:
  - You want zero extra dependencies beyond the Python standard library.
  - You have maximum performance/low-overhead requirements.
  - You do not need runtime type casting or JSON Schema exports.

- **Choose Pydantic v2** (`--output pydantic`) if:
  - You are integrating with **FastAPI** or modern API frameworks.
  - You need automatic data validation (e.g. `min_length`, regex patterns, numerical bounds).
  - You want out-of-the-box `.model_dump()` and `.model_json_schema()` capabilities.

---

### How do I configure custom XML namespace prefixes when serializing?

When serializing models, you can map namespace URIs to clean prefixes using `ns_map` on `XmlSerializer`:

```python
from pyxsdata.formats.dataclass.serializers import XmlSerializer
from pyxsdata.formats.dataclass.serializers.config import SerializerConfig

ns_map = {
    None: "http://example.com/default",  # Default namespace (no prefix)
    "inv": "http://example.com/invoice",
    "cust": "http://example.com/customer",
}

serializer = XmlSerializer(config=SerializerConfig(pretty_print=True))
xml_output = serializer.render(my_model, ns_map=ns_map)
```

---

### How do I parse very large XML files without high memory usage?

By default, `XmlParser` streams XML elements event-by-event rather than loading the whole DOM into memory. If your document has millions of repeating child items (e.g. `<record>` in `<database>`), you can use selective parsing:

```python
from pyxsdata.formats.dataclass.parsers import XmlParser
from myapp.models import Record

parser = XmlParser()

# Pass a generator or stream handler to process records one-by-one:
with open("huge_data.xml", "rb") as fp:
    # Target specific element types
    record = parser.parse(fp, Record)
```

For maximum throughput on large files, use `PugixmlEventHandler`:

```python
from pyxsdata.formats.dataclass.parsers.handlers import PugixmlEventHandler

parser = XmlParser(handler=PugixmlEventHandler)
data = parser.parse("huge_feed.xml", FeedModel)
```

---

### How do I use `pyxsdata` with FastAPI?

Because `pyxsdata.pydantic` models are standard Pydantic `BaseModel` subclasses, you can use them directly in FastAPI routes:

```python
from fastapi import FastAPI, Response
from myapp.models import PurchaseOrder
from pyxsdata.pydantic.bindings import XmlParser, XmlSerializer

app = FastAPI()
parser = XmlParser()
serializer = XmlSerializer()

@app.post("/order", response_model=PurchaseOrder)
async def create_order(order: PurchaseOrder):
    # FastAPI automatically validates incoming JSON into the Pydantic model
    return order

@app.get("/order/{order_id}/xml")
async def get_order_xml(order_id: str):
    order = fetch_order(order_id)
    xml_data = serializer.render(order)
    return Response(content=xml_data, media_type="application/xml")
```

---

### Why are some non-nullable fields marked with `kw_only=True`?

In standard Python dataclasses, declaring a non-default field after a field with a default value causes a `TypeError: non-default argument follows default argument`.

In XML schemas, elements can be in any sequence, meaning an optional element often precedes a required element. `pyxsdata` targets Python 3.12+ and generates all dataclasses with `@dataclass(kw_only=True)`, cleanly solving the ordering issue while keeping required fields non-nullable.

---

### Why are elements serialized in a different order than expected?

In XML Schema, order can be strictly enforced (`xs:sequence`) or flexible (`xs:all`, `xs:choice`). If your schema has multiple mixed choices or overlapping elements, enable compound fields in the generator:

```console
$ pyxsdata generate schema.xsd --compound-fields
```

This groups mixed child elements into a single list while preserving the exact order they appeared in the XML source.

---

### How can I convert directly between XML and JSON?

You can easily round-trip between XML and JSON using `XmlParser` and `JsonSerializer`:

```python
from pyxsdata.formats.dataclass.parsers import XmlParser
from pyxsdata.formats.dataclass.serializers import JsonSerializer
from myapp.models import Catalog

# 1. Parse XML
xml_parser = XmlParser()
catalog = xml_parser.parse("catalog.xml", Catalog)

# 2. Serialize to JSON
json_serializer = JsonSerializer(indent="  ")
json_str = json_serializer.render(catalog)
print(json_str)
```
