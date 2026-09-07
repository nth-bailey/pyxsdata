# Modern XML & JSON Data Binding for Python 3.12+

[![CI Tests](https://github.com/nth-bailey/pyxsdata/workflows/tests/badge.svg)](https://github.com/nth-bailey/pyxsdata/actions)
[![Documentation](https://github.com/nth-bailey/pyxsdata/actions/workflows/docs.yml/badge.svg)](https://nth-bailey.github.io/pyxsdata/)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/nth-bailey/pyxsdata/actions/workflows/tests.yml)
[![PyPI version](https://img.shields.io/pypi/v/pyxsdata.svg)](https://pypi.org/project/pyxsdata/)
[![Python versions](https://img.shields.io/pypi/pyversions/pyxsdata.svg)](https://pypi.org/project/pyxsdata/)

---

**pyxsdata** is a modern, high-performance data binding and code generation library for
Python 3.12+. It allows developers to seamlessly convert XML and JSON documents into
native Python objects (**Standard Dataclasses** or **Pydantic v2** models) rather than
dealing directly with the DOM.

!!! info "A Modern Successor to xsdata"

    **pyxsdata** is an actively maintained, modernized fork of [`xsdata`](https://github.com/tefra/xsdata) designed exclusively for Python 3.12+. It consolidates ecosystem extensions like `xsdata-pydantic` directly into the unified core, introduces ultra-fast C++ **pugixml** pull-parsing support, leverages modern PEP 695 generics, and is built with modern tooling ([uv](https://github.com/astral-sh/uv), [ty](https://docs.astral.sh/ty/), and [ruff](https://docs.astral.sh/ruff/)).

---

## ⚡ Quick Start

=== "1. Installation"

    ```console
    $ pip install "pyxsdata[cli,lxml,soap,pydantic]"
    ```

    !!! tip "Installation Extras"
        - `cli`: Command-line interface and code generator
        - `pydantic`: Native Pydantic v2 bindings and code generation
        - `lxml`: High-performance C-based XML parsing
        - `soap`: SOAP client webservice transport

=== "2. Code Generation"

    Generate Python dataclasses or Pydantic models from any schema:

    ```console
    # Generate standard dataclasses
    $ pyxsdata generate schema.xsd --package myapp.models

    # Or generate native Pydantic v2 models
    $ pyxsdata generate schema.xsd --output pydantic --package myapp.models
    ```

=== "3. Dataclass Binding"

    Parse and serialize XML with standard Python dataclasses:

    ```python
    from pyxsdata.formats.dataclass.parsers import XmlParser
    from pyxsdata.formats.dataclass.serializers import XmlSerializer
    from pyxsdata.formats.dataclass.serializers.config import SerializerConfig
    from myapp.models import PurchaseOrder

    # Parsing
    parser = XmlParser()
    order = parser.parse("order.xml", PurchaseOrder)
    print(order.bill_to.name)  # "Robert Smith"

    # Serializing
    config = SerializerConfig(pretty_print=True)
    serializer = XmlSerializer(config=config)
    xml_output = serializer.render(order)
    ```

=== "4. Pydantic v2 Binding"

    Drop-in XML parsing and serialization using Pydantic models:

    ```python
    from pyxsdata.pydantic.bindings import XmlParser, XmlSerializer
    from myapp.models import PurchaseOrder

    parser = XmlParser()
    order = parser.from_string(xml_text, PurchaseOrder)

    # Full Pydantic v2 features:
    data_dict = order.model_dump()
    json_schema = order.model_json_schema()

    serializer = XmlSerializer()
    xml_output = serializer.render(order)
    ```

---

## 🌟 Key Features

- **Unified Schema Support**: Generate models from W3C XML Schema (XSD 1.0 & 1.1), WSDL
  1.1, DTD definitions, and raw XML or JSON documents.
- **Native Pydantic v2**: Built-in first-class Pydantic v2 code generator and binding
  layer (`pyxsdata.pydantic`). No external plugins required.
- **Blazing Fast Performance**: Up to **25% faster** XML deserialization than legacy
  `xsdata` through zero-overhead type conversion, MRO caching, short-circuited attribute
  checks, and native support for `xml.etree`, `lxml`, and C++ `pugixml`.
- **Modern Python 3.12+**: Strictly built for Python 3.12+. Fully type-annotated, PEP
  695 generics, and verified with Astral `ty` with zero diagnostics.

---

## 💡 The Philosophy

!!! note "Why naive?" The W3C XML Schema specification is notoriously complex because it
was designed to accommodate every conceivable document layout. When consuming schemas in
application code, developers simply need clean, intuitive data structures.

    `pyxsdata` simplifies XML binding through an elegant core assumption:

    > **All schema definitions are classes; everything else is class properties.**

---

## 📚 Explore the Documentation

- [5-Minute Quickstart](quickstart.md) - Get up and running in minutes with a complete
  step-by-step tutorial.
- [Installation Guide](installation.md) - Learn about optional dependencies, `uv`, and
  verification.
- [Migrating from xsdata](migration.md) - Seamlessly migrate existing codebases to
  pyxsdata and native Pydantic v2.
- [Code Generator Guide](codegen/intro.md) - Explore CLI options, configurations, and
  docstring styles.
- [Data Binding Guide](data_binding/basics.md) - Learn XML/JSON parsing, serialization,
  and tree manipulation.
- [Parser Backends](data_binding/backends.md) - Compare performance between standard
  library, `lxml`, and `pugixml`.
- [Pydantic v2 Integration](pydantic/index.md) - Deep dive into native Pydantic v2
  models and JSON schema support.
- [Frequently Asked Questions](faq.md) - Solutions to common questions, large file
  streaming, and web framework tips.
- [Sample Projects](samples.md) - Real-world schemas and models in action.
- [Changelog](changelog.md) - Release notes and version history.
