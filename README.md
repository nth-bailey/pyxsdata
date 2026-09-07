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

- **Significantly Faster Deserialization**: Up to **54% faster** in pure Python (over
  **2x throughput**) and up to **15x faster** with native Rust acceleration
  (`pyxsdata[core]`) compared to legacy `xsdata`.
- **Unified Native Pydantic v2**: Consolidates `xsdata-pydantic` directly into the core
  library under `pyxsdata.pydantic` with dedicated `--output pydantic` generation and
  drop-in parsers/serializers.
- **Python 3.12+ Architecture**: Exclusively leverages PEP 695 generics
  (`class Foo[T]: ...`), type union syntax (`X | Y`), pattern matching, and `kw_only`
  dataclasses.
- **Native Rust Acceleration (`pyxsdata-core`)**: First-class zero-copy Rust parser
  backend achieving **~300,000+ objects/sec** (`pip install "pyxsdata[core]"`).
- **Ultra-Fast C++ pugixml Support**: First-class support for constant-memory
  pull-parsing via [pugixml](https://pugixml.org/) (`pip install "pyxsdata[pugixml]"`).
- **Modern Packaging & Tooling**: Managed and built with Astral
  [`uv`](https://github.com/astral-sh/uv), statically type checked with Astral `ty` with
  zero diagnostics, and formatted with `ruff`.
- **Active & Responsive Maintenance**: Regular dependency updates, modern CI packaging,
  and active community maintenance.

## Performance & Deserializer Benchmarks

`pyxsdata` provides a decoupled, event-driven deserialization architecture supporting
multiple parser backends. You can freely choose between zero-dependency standard library
execution, C/C++ acceleration, or native Rust parsing via
[`pyxsdata-core`](https://github.com/nth-bailey/pyxsdata-core).

### Deserialization Benchmarks (Standard Python `@dataclass`)

Parsing **10,000 complex XML items** (3.36 MB payload) into nested Python `@dataclass`
structures:

| Deserializer / Handler                       | Engine                        | Extra Dependency    | Legacy `xsdata` | `pyxsdata`   | Throughput          | Speedup vs Legacy          |
| :------------------------------------------- | :---------------------------- | :------------------ | :-------------- | :----------- | :------------------ | :------------------------- |
| **`CoreEventHandler`** / **`CoreXmlParser`** | **Rust + PyO3 (`quick-xml`)** | `pyxsdata[core]`    | ~513.0 ms       | **34.4 ms**  | **~290,700 objs/s** | **~15.0x (1,490% faster)** |
| **`NativeEventHandler`**                     | Python `xml.etree`            | _None (built-in)_   | 728.9 ms        | **332.5 ms** | ~30,075 objs/s      | **+54.4% (2.2x faster)**   |
| **`LxmlEventHandler`**                       | C `libxml2` (`lxml`)          | `pyxsdata[lxml]`    | 753.2 ms        | **375.2 ms** | ~26,650 objs/s      | **+50.2% (2.0x faster)**   |
| **`PugixmlEventHandler`**                    | C++ `pugixml` (`pygixml`)     | `pyxsdata[pugixml]` | 883.8 ms        | **509.4 ms** | ~19,630 objs/s      | **+42.4% (1.7x faster)**   |

_(Benchmark run on Linux x86_64, CPython 3.12.14, lowest of 5 runs over 10,000 items)_

### Deserialization Benchmarks (Pydantic v2 `BaseModel`)

Parsing **1,000 complex XML items** into Pydantic v2 `BaseModel` instances:

| Deserializer                              | Engine                        | Latency (1,000 items) | Throughput          | Speedup                       |
| :---------------------------------------- | :---------------------------- | :-------------------- | :------------------ | :---------------------------- |
| **`CoreXmlParser`** (`pyxsdata.pydantic`) | **Rust + PyO3 (`quick-xml`)** | **3.2 ms**            | **~311,245 objs/s** | **~7.67x faster (767%)**      |
| **`XmlParser`** (`pyxsdata.pydantic`)     | Pure Python (`xml.etree`)     | 24.6 ms               | ~40,580 objs/s      | 1.0x (Baseline)               |
| **Legacy `xsdata-pydantic`**              | Pure Python (`xml.etree`)     | 38.2 ms               | ~26,170 objs/s      | 0.64x (~11.9x slower vs Core) |

### Which Deserializer Should You Use?

- **`CoreXmlParser` / `CoreEventHandler` (`pip install "pyxsdata[core]"`):**
  **Recommended for high-throughput production systems**, real-time APIs, webhooks, and
  big data feeds. Driven by native Rust (`quick-xml`), it bypasses intermediate Python
  DOM objects and maps tokens directly to Python dataclasses or Pydantic models via
  CPython C-API at **~300,000 objects/second**.
- **`NativeEventHandler` (Built-in standard library):** **Recommended for
  zero-dependency deployments**, lightweight microservices, and serverless environments
  (AWS Lambda, Google Cloud Run) where installing C/Rust compilers is undesirable.
- **`LxmlEventHandler` (`pip install "pyxsdata[lxml]"`):** Ideal for legacy XML
  workflows requiring schema DTD validation (`load_dtd=True`), XInclude resolution
  (`process_xinclude=True`), or direct parsing from `lxml.etree.Element` trees.
- **`PugixmlEventHandler` (`pip install "pyxsdata[pugixml]"`):** Fast C++ pull-parser
  offering constant-memory streaming for large XML payloads.

## Getting started

```console
$ # Install all dependencies including CLI, LXML, SOAP, Pydantic, and native Rust core acceleration
$ pip install "pyxsdata[cli,core,lxml,soap,pydantic]"
```

```console
$ # Generate models
$ pyxsdata generate tests/fixtures/primer/order.xsd --package tests.fixtures.primer
```

```python
>>> from tests.fixtures.primer import PurchaseOrder
>>> from pyxsdata.formats.dataclass.parsers import XmlParser, CoreXmlParser
>>>
>>> # Standard pure Python parser:
>>> parser = XmlParser()
>>> order = parser.parse("tests/fixtures/primer/sample.xml", PurchaseOrder)
>>> order.bill_to
Usaddress(name='Robert Smith', street='8 Oak Avenue', city='Old Town', state='PA', zip=Decimal('95819'), country='US')
>>>
>>> # Or ultra-fast Rust-accelerated parser (~290,000+ objs/sec):
>>> core_parser = CoreXmlParser()
>>> order = core_parser.parse("tests/fixtures/primer/sample.xml", PurchaseOrder)
```

### Pydantic Support

Generate Pydantic v2 models directly with `--output pydantic`:

```console
$ pyxsdata generate tests/fixtures/primer/order.xsd --output pydantic --package myapp.models
```

```python
>>> from pyxsdata.pydantic.bindings import XmlParser, CoreXmlParser
>>>
>>> # Standard pure Python parser:
>>> parser = XmlParser()
>>> order = parser.from_string(xml_text, PurchaseOrder)
>>> order.model_dump()
>>>
>>> # Or ultra-fast Rust-accelerated parser (~310,000+ objs/sec):
>>> core_parser = CoreXmlParser()
>>> order = core_parser.from_string(xml_text, PurchaseOrder)
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
- Multiple parser handlers: Native `xml.etree`, C `lxml`, C++ `pugixml`, and Rust
  `pyxsdata-core`
- Native Rust zero-copy acceleration (`pyxsdata-core`) for ~300k objs/sec
  deserialization
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
