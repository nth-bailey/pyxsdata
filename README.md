# Modern XML & JSON Bindings for Python 3.12+

[![image](https://github.com/nth-bailey/pyxsdata/workflows/tests/badge.svg)](https://github.com/nth-bailey/pyxsdata/actions)
[![docs](https://github.com/nth-bailey/pyxsdata/actions/workflows/docs.yml/badge.svg)](https://nth-bailey.github.io/pyxsdata/)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/nth-bailey/pyxsdata/actions/workflows/tests.yml)
[![image](https://img.shields.io/pypi/pyversions/pyxsdata.svg)](https://pypi.org/pypi/pyxsdata/)
[![image](https://img.shields.io/pypi/v/pyxsdata.svg)](https://pypi.org/pypi/pyxsdata/)

---

pyxsdata is a complete, modern data binding library for Python 3.12+ allowing developers
to access and use XML and JSON documents as simple objects rather than using DOM.

The code generator supports XML schemas, DTD, WSDL definitions, XML & JSON documents. It
produces simple dataclasses or Pydantic v2 models with type hints and binding metadata.

The included XML and JSON parser/serializer are highly optimized and adaptable, with
multiple handlers and configuration properties.

## About `pyxsdata` (Modern Fork of `xsdata`)

`pyxsdata` is a modernized successor and fork of
[`xsdata`](https://github.com/tefra/xsdata) designed exclusively for Python 3.12+ and
actively maintained with modern tooling.

### Key Enhancements over Legacy xsdata

- **Unified Native Pydantic v2**: Consolidates `xsdata-pydantic` directly into the core
  library under `pyxsdata.pydantic` with dedicated `--output pydantic` generation and
  drop-in parsers/serializers.
- **Python 3.12+ Architecture**: Exclusively leverages PEP 695 generics
  (`class Foo[T]: ...`), type union syntax (`X | Y`), pattern matching, and `kw_only`
  dataclasses.
- **Ultra-Fast C++ pugixml Support**: First-class support for constant-memory
  pull-parsing via [pugixml](https://pugixml.org/) (`pip install "pyxsdata[pugixml]"`).
- **Modern Packaging & Tooling**: Managed and built with Astral
  [`uv`](https://github.com/astral-sh/uv), statically type checked with Astral `ty` with
  zero diagnostics, and formatted with `ruff`.
- **Active & Responsive Maintenance**: Regular dependency updates, modern CI packaging,
  and active community maintenance.

## Getting started

```console
$ # Install all dependencies including CLI, LXML, SOAP, and Pydantic
$ pip install "pyxsdata[cli,lxml,soap,pydantic]"
```

```console
$ # Generate models
$ pyxsdata generate tests/fixtures/primer/order.xsd --package tests.fixtures.primer
```

```python
>>> from tests.fixtures.primer import PurchaseOrder
>>> from pyxsdata.formats.dataclass.parsers import XmlParser
>>>
>>> parser = XmlParser()
>>> order = parser.parse("tests/fixtures/primer/sample.xml", PurchaseOrder)
>>> order.bill_to
Usaddress(name='Robert Smith', street='8 Oak Avenue', city='Old Town', state='PA', zip=Decimal('95819'), country='US')
```

### Pydantic Support

Generate Pydantic v2 models directly with `--output pydantic`:

```console
$ pyxsdata generate tests/fixtures/primer/order.xsd --output pydantic --package myapp.models
```

```python
>>> from pyxsdata.pydantic.bindings import XmlParser
>>> parser = XmlParser()
>>> order = parser.from_string(xml_text, PurchaseOrder)
>>> order.model_dump()
```

Check the [documentation](https://nth-bailey.github.io/pyxsdata/) for more ✨✨✨

## Features

**Code Generator**

- XML Schemas 1.0 & 1.1
- WSDL 1.1 definitions with SOAP 1.1 bindings
- DTD external definitions
- Directly from XML and JSON Documents
- Extensive configuration to customize output
- Pluggable code writer for custom output formats (Standard Dataclasses, Pydantic v2)

**Default Output**

- Pure Python 3.12+ dataclasses or Pydantic models with metadata
- Modern type hints with support for forward references and unions
- Enumerations and inner classes
- Support namespace qualified elements and attributes

**Data Binding**

- XML and JSON parser, serializer
- PyCode serializer
- Handlers and Writers based on lxml and native xml python
- Support wildcard elements and attributes
- Support xinclude statements and unknown properties
- Native Pydantic v2 support (`pyxsdata.pydantic`)
- Fully type-checked with Astral `ty`

## Changelog: 0.0.0

- Modernized for Python 3.12+ minimum.
- Consolidated `xsdata-pydantic` into core library as `pyxsdata.pydantic`.
- Replaced mypy with Astral's static type checker `ty`.
- Standardized CLI tool to `pyxsdata`.
- Documentation powered by Zensical.
