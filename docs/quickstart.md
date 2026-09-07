# 5-Minute Quickstart

Welcome! In this quick tutorial, you'll learn how to take an XML schema or document, generate typed Python models, parse XML files into Python objects with full IDE autocomplete, and serialize them back to XML.

---

## 1. Installation

Install `pyxsdata` with the CLI and your preferred features:

=== "Using uv"

    ```console
    $ uv add "pyxsdata[cli,pydantic,pugixml]"
    ```

=== "Using pip"

    ```console
    $ pip install "pyxsdata[cli,pydantic,pugixml]"
    ```

---

## 2. Prepare an XML Schema or Document

Suppose you have a sample schema describing a bookstore catalog, `catalog.xsd`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="catalog">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="book" maxOccurs="unbounded">
          <xs:complexType>
            <xs:sequence>
              <xs:element name="title" type="xs:string"/>
              <xs:element name="author" type="xs:string"/>
              <xs:element name="price" type="xs:decimal"/>
            </xs:sequence>
            <xs:attribute name="id" type="xs:string" use="required"/>
            <xs:attribute name="available" type="xs:boolean" default="true"/>
          </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
```

And an incoming XML document, `catalog.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<catalog>
  <book id="bk101" available="true">
    <title>The Python Standard Library</title>
    <author>Guido van Rossum</author>
    <price>29.99</price>
  </book>
  <book id="bk102" available="false">
    <title>Designing Data-Intensive Applications</title>
    <author>Martin Kleppmann</author>
    <price>44.99</price>
  </book>
</catalog>
```

---

## 3. Generate Python Models

Run `pyxsdata generate` pointing to your schema or sample XML:

=== "Standard Dataclasses"

    ```console
    $ pyxsdata generate catalog.xsd --package myapp.models
    ```

=== "Pydantic v2 Models"

    ```console
    $ pyxsdata generate catalog.xsd --output pydantic --package myapp.models
    ```

`pyxsdata` generates type-safe Python code formatted with [Ruff](https://docs.astral.sh/ruff/). Notice how clean the generated code is:

=== "Generated Dataclass (myapp/models.py)"

    ```python
    from dataclasses import dataclass, field
    from decimal import Decimal

    @dataclass(kw_only=True)
    class Catalog:
        @dataclass(kw_only=True)
        class Book:
            title: str = field(metadata={"type": "Element", "required": True})
            author: str = field(metadata={"type": "Element", "required": True})
            price: Decimal = field(metadata={"type": "Element", "required": True})
            id: str = field(metadata={"type": "Attribute", "required": True})
            available: bool = field(default=True, metadata={"type": "Attribute"})

        book: list[Book] = field(
            default_factory=list,
            metadata={"type": "Element", "min_occurs": 1},
        )
    ```

=== "Generated Pydantic v2 (myapp/models.py)"

    ```python
    from decimal import Decimal
    from pydantic import BaseModel, Field

    class Catalog(BaseModel):
        class Book(BaseModel):
            title: str = Field(metadata={"type": "Element", "required": True})
            author: str = Field(metadata={"type": "Element", "required": True})
            price: Decimal = Field(metadata={"type": "Element", "required": True})
            id: str = Field(metadata={"type": "Attribute", "required": True})
            available: bool = Field(default=True, metadata={"type": "Attribute"})

        book: list[Book] = Field(
            default_factory=list,
            metadata={"type": "Element", "min_occurs": 1},
        )
    ```

---

## 4. Parse XML into Python Objects

Load and parse XML files, strings, or streams in just three lines:

=== "Using Standard Dataclasses"

    ```python
    from pyxsdata.formats.dataclass.parsers import XmlParser
    from myapp.models import Catalog

    # Initialize parser
    parser = XmlParser()

    # Parse from file, string, or bytes
    catalog = parser.parse("catalog.xml", Catalog)

    # Full IDE autocompletion & type safety
    for book in catalog.book:
        status = "In stock" if book.available else "Sold out"
        print(f"[{book.id}] {book.title} by {book.author} - ${book.price} ({status})")
    ```

=== "Using Pydantic v2"

    ```python
    from pyxsdata.pydantic.bindings import XmlParser
    from myapp.models import Catalog

    parser = XmlParser()
    catalog = parser.parse("catalog.xml", Catalog)

    # Access Pydantic v2 methods
    print(catalog.model_dump())
    print(catalog.model_json_schema())
    ```

---

## 5. Modify and Serialize Back to XML

Modify your typed models in Python and serialize them back to beautiful, formatted XML:

```python
from decimal import Decimal
from pyxsdata.formats.dataclass.serializers import XmlSerializer
from pyxsdata.formats.dataclass.serializers.config import SerializerConfig
from myapp.models import Catalog

# Add a new book
catalog.book.append(
    Catalog.Book(
        id="bk103",
        title="Fluent Python",
        author="Luciano Ramalho",
        price=Decimal("39.99"),
        available=True,
    )
)

# Configure pretty printing and indentation
config = SerializerConfig(pretty_print=True, indent="  ")
serializer = XmlSerializer(config=config)

# Render to XML string
xml_output = serializer.render(catalog)
print(xml_output)
```

**Output:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<catalog>
  <book id="bk101" available="true">
    <title>The Python Standard Library</title>
    <author>Guido van Rossum</author>
    <price>29.99</price>
  </book>
  <book id="bk102" available="false">
    <title>Designing Data-Intensive Applications</title>
    <author>Martin Kleppmann</author>
    <price>44.99</price>
  </book>
  <book id="bk103" available="true">
    <title>Fluent Python</title>
    <author>Luciano Ramalho</author>
    <price>39.99</price>
  </book>
</catalog>
```

---

## 6. Next Steps

Now that you have seen the basics, explore the rest of the documentation:

- [Parser Backends Guide](data_binding/backends.md) — Learn how to speed up XML parsing with C++ **pugixml** or **lxml**.
- [Pydantic v2 Guide](pydantic/index.md) — Integrate pyxsdata with FastAPI, JSON schema export, and data validation.
- [Code Generator Guide](codegen/intro.md) — Customize package naming, class filters, docstrings, and config files.
- [Data Binding Deep Dive](data_binding/basics.md) — Work with JSON, raw dictionaries, XML trees, and streaming iterparse.
