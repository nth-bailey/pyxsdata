# Modern XML & JSON Bindings for Python 3.12+

[![image](https://github.com/nth-bailey/pyxsdata/workflows/tests/badge.svg)](https://github.com/nth-bailey/pyxsdata/actions)
[![image](https://readthedocs.org/projects/pyxsdata/badge)](https://pyxsdata.readthedocs.io/)
[![image](https://codecov.io/gh/nth-bailey/pyxsdata/branch/main/graph/badge.svg)](https://codecov.io/gh/nth-bailey/pyxsdata)
[![image](https://img.shields.io/pypi/pyversions/pyxsdata.svg)](https://pypi.org/pypi/pyxsdata/)
[![image](https://img.shields.io/pypi/v/pyxsdata.svg)](https://pypi.org/pypi/pyxsdata/)

---

pyxsdata is a complete, modern data binding library for Python 3.12+ allowing developers to access and
use XML and JSON documents as simple objects rather than using DOM.

The code generator supports XML schemas, DTD, WSDL definitions, XML & JSON documents. It
produces simple dataclasses or Pydantic v2 models with type hints and binding metadata.

The included XML and JSON parser/serializer are highly optimized and adaptable, with
multiple handlers and configuration properties.

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

Check the [documentation](https://pyxsdata.readthedocs.io) for more ✨✨✨

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

## Changelog: 26.3.0

- Modernized for Python 3.12+ minimum.
- Consolidated `xsdata-pydantic` into core library as `pyxsdata.pydantic`.
- Replaced mypy with Astral's static type checker `ty`.
- Standardized CLI tool to `pyxsdata`.
- Documentation powered by Zensical.
