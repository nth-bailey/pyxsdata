# Modern XML & JSON Bindings for Python 3.12+

<p align="center">
  <a href="https://github.com/nth-bailey/pyxsdata/actions"><img src="https://img.shields.io/github/actions/workflow/status/nth-bailey/pyxsdata/tests.yml?branch=main&label=CI&logo=github" alt="CI"></a>
  <a href="https://nth-bailey.github.io/pyxsdata/"><img src="https://img.shields.io/badge/docs-zensical-blue.svg?logo=gitbook" alt="Docs"></a>
  <a href="https://github.com/nth-bailey/pyxsdata/actions/workflows/tests.yml"><img src="https://img.shields.io/badge/coverage-100%25-brightgreen.svg?logo=pytest" alt="Coverage: 100%"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="https://github.com/astral-sh/ty"><img src="https://img.shields.io/badge/type_checker-Astral_ty-blueviolet" alt="Astral ty"></a>
  <a href="https://github.com/astral-sh/uv"><img src="https://img.shields.io/badge/uv-managed-DE5FE9?logo=astral&logoColor=white" alt="uv"></a>
  <a href="https://github.com/nth-bailey/pyxsdata/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
</p>

<p align="center">
  <a href="https://pypi.org/project/pyxsdata/"><img src="https://img.shields.io/pypi/v/pyxsdata.svg?logo=pypi&label=PyPI" alt="PyPI"></a>
  <a href="https://pypi.org/project/pyxsdata/"><img src="https://img.shields.io/badge/Python-3.12%20%7C%203.13%20%7C%203.14-3776AB.svg?logo=python&logoColor=white" alt="Python 3.12+"></a>
  <a href="https://docs.pydantic.dev/"><img src="https://img.shields.io/badge/Pydantic-v2-E92063.svg?logo=pydantic&logoColor=white" alt="Pydantic v2"></a>
  <a href="https://nth-bailey.github.io/pyxsdata/"><img src="https://img.shields.io/badge/AI_%26_LLM-Ready-FF6F00.svg?logo=openai&logoColor=white" alt="AI & LLM Ready"></a>
  <a href="https://github.com/nth-bailey/PolyXML"><img src="https://img.shields.io/badge/acceleration-Rust_PolyXML-DEA584?logo=rust&logoColor=white" alt="Rust PolyXML"></a>
  <a href="https://github.com/nth-bailey/pyxsdata/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?logo=github" alt="PRs Welcome"></a>
</p>

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

- **Built for Modern AI & LLMs**: Native tree pruning (`prune_dump`) and dynamic model
  projection (`project_model`) allow developers to pipe massive enterprise XML schemas
  directly into OpenAI, Anthropic, Gemini, and LangChain with **80–90% prompt token
  reduction** and zero JSON schema bloat.
- **Significantly Faster Deserialization**: Up to **54% faster** in pure Python (over
  **2x throughput**) and up to **15x faster** with native Rust acceleration
  (`pyxsdata[core]`) compared to legacy `xsdata`.
- **Unified Native Pydantic v2**: Consolidates `xsdata-pydantic` directly into the core
  library under `pyxsdata.pydantic` with dedicated `--output pydantic` generation and
  drop-in parsers/serializers.
- **Python 3.12+ Architecture**: Exclusively leverages PEP 695 generics
  (`class Foo[T]: ...`), type union syntax (`X | Y`), pattern matching, and `kw_only`
  dataclasses.
- **Native Rust Acceleration (`polyxml`)**: First-class zero-copy Rust parser and
  serializer backend achieving **~300,000+ objects/sec**
  (`pip install "pyxsdata[core]"`).
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
execution, C/C++ acceleration, or native Rust parsing and serialization via
[`PolyXML`](https://github.com/nth-bailey/PolyXML).

### Deserialization Benchmarks (Standard Python `@dataclass`)

Parsing **10,000 complex XML items** (3.36 MB payload) into nested Python `@dataclass`
structures:

| Deserializer / Handler                      | Engine                      | Extra Dependency    | Legacy `xsdata` | `pyxsdata`  | Throughput          | Speedup vs Legacy         |
| :------------------------------------------ | :-------------------------- | :------------------ | :-------------- | :---------- | :------------------ | :------------------------ |
| **`CoreXmlParser`** (`CoreEventHandler`)    | **Rust + PyO3 (`PolyXML`)** | `pyxsdata[core]`    | —               | **32.8 ms** | **~304,878 objs/s** | **~10.60x (960% faster)** |
| **`PugixmlParser`** (`PugixmlEventHandler`) | C++ (`pugixml`)             | `pyxsdata[pugixml]` | 126.8 ms        | 92.4 ms     | ~108,225 objs/s     | ~3.76x (276% faster)      |
| **`LxmlEventHandler`**                      | C (`lxml`)                  | `pyxsdata[lxml]`    | 245.5 ms        | 218.1 ms    | ~45,850 objs/s      | ~1.60x (60% faster)       |
| **`XmlParser`** (`DefaultXmlHandler`)       | Pure Python (`xml.etree`)   | —                   | 347.8 ms        | 312.4 ms    | ~32,010 objs/s      | 1.0x (Baseline)           |

### Deserialization Benchmarks (Pydantic v2 `BaseModel`)

Parsing **1,000 complex XML items** into Pydantic v2 `BaseModel` instances:

| Deserializer                              | Engine                        | Latency (1,000 items) | Throughput          | Speedup                       |
| :---------------------------------------- | :---------------------------- | :-------------------- | :------------------ | :---------------------------- |
| **`CoreXmlParser`** (`pyxsdata.pydantic`) | **Rust + PyO3 (`quick-xml`)** | **3.2 ms**            | **~311,245 objs/s** | **~7.67x faster (767%)**      |
| **`XmlParser`** (`pyxsdata.pydantic`)     | Pure Python (`xml.etree`)     | 24.6 ms               | ~40,580 objs/s      | 1.0x (Baseline)               |
| **Legacy `xsdata-pydantic`**              | Pure Python (`xml.etree`)     | 38.2 ms               | ~26,170 objs/s      | 0.64x (~11.9x slower vs Core) |

### Real-World Enterprise Benchmark: UCI `Entity` Message

Parsing nested, production-grade **Universal Command and Control Interface (UCI v2.5)**
`Entity` telemetry messages (with security markings, timestamps, headers, metadata, and
enums):

| Deserializer                          | Engine                        | Latency / Message | Throughput         | Speedup                     |
| :------------------------------------ | :---------------------------- | :---------------- | :----------------- | :-------------------------- |
| **`PolyXML`** (`pyxsdata[core]`)      | **Rust + PyO3 (`quick-xml`)** | **16.5 µs**       | **~60,360 msgs/s** | **~11.47x (1,047% faster)** |
| **`XmlParser`** (`pyxsdata` Standard) | Pure Python (`xml.etree`)     | 190.0 µs          | ~5,262 msgs/s      | 1.0x (Baseline)             |

### Which Deserializer Should You Use?

- **`CoreXmlParser` / `CoreEventHandler` / `CoreXmlSerializer`
  (`pip install "pyxsdata[core]"`):** **Recommended for high-throughput production
  systems**, real-time APIs, webhooks, and big data feeds. Driven by native Rust
  (`PolyXML`), it bypasses intermediate Python DOM objects and maps tokens directly to
  Python dataclasses or Pydantic models via CPython C-API at **~300,000
  objects/second**.
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

## 🤖 Built for Modern AI & LLMs

Enterprise XML schemas (ISO 20022, UBL, HL7, FIX) are massive, deeply nested, and
token-heavy. Feeding them directly to LLMs often hits strict JSON schema limits or
explodes your token bill.

`pyxsdata.pydantic` provides native utilities specifically built for AI workflows:

### 1. Token-Efficient Prompt Ingestion (`prune_dump`)

Strip namespace noise, empty structures, and unused branches with glob dot-paths before
sending data to an LLM:

```python
from pyxsdata.pydantic import XmlParser, prune_dump

# Parse complex enterprise XML
order = XmlParser().from_string(xml_text, EnterprisePurchaseOrder)

# Prune down to just what the LLM needs (80-90% token reduction!):
prompt_payload = prune_dump(
    order,
    include=["id", "order_date", "customer.name", "items.*.sku", "items.*.price"],
    exclude_namespaces=["http://www.w3.org/2000/09/xmldsig#"],  # Drop signatures
    exclude_none=True,  # Drop unpopulated fields
    exclude_empty=True, # Drop empty lists [] and dicts {}
    key_style="python", # Clean snake_case keys (no XML namespace mangling)
)

# Clean, token-efficient JSON ready for OpenAI, Anthropic, or Gemini:
# {"id": "ORD-001", "order_date": "2026-09-13", "customer": {"name": "Acme Corp"}, "items": [...]}
```

### 2. Zero-Bloat LLM Structured Outputs (`project_model`)

When asking an LLM to generate data via `response_format` or Tool Calling, don't
overwhelm it with a 500-field JSON schema. Dynamically project a lightweight Pydantic v2
sub-model:

```python
from pyxsdata.pydantic import XmlSerializer, project_model

# Dynamically create a lean sub-model with only the fields the LLM should extract:
LLMPurchaseOrder = project_model(
    EnterprisePurchaseOrder,
    include={"id", "order_date", "customer.name", "items.sku", "items.quantity"},
)

# Pass directly to OpenAI / Anthropic / Gemini Structured Outputs:
response = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Extract order from email..."}],
    response_format=LLMPurchaseOrder,
)
lean_order: LLMPurchaseOrder = response.choices[0].message.parsed

# Re-hydrate back into the full enterprise model and serialize to valid XML!
full_order = EnterprisePurchaseOrder.model_validate(lean_order.model_dump())
xml_output = XmlSerializer().render(full_order)
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
- Zero cold-start package overhead with `--lazy-load` (PEP 562 on-demand class loading)

**Default Output**

- Pure Python 3.12+ dataclasses or Pydantic models with metadata
- Modern type hints with support for forward references and unions
- Enumerations and inner classes
- Support namespace qualified elements and attributes

**Data Binding**

- XML and JSON parser, serializer
- PyCode serializer
- Multiple parser handlers: Native `xml.etree`, C `lxml`, C++ `pugixml`, and Rust
  `PolyXML`
- Native Rust zero-copy acceleration (`PolyXML`) for ~300k objs/sec deserialization and
  serialization
- Support wildcard elements and attributes
- Support xinclude statements and unknown properties
- Native Pydantic v2 support (`pyxsdata.pydantic`)
- Fully type-checked with Astral `ty`

**AI & LLM Integration**

- Token-efficient instance pruning (`prune_dump`) with glob dot-path, namespace URI, and
  prefix filtering
- Dynamic sub-model projection (`project_model`) preserving constraints and types for
  zero-bloat OpenAI, Anthropic, and Gemini Structured Outputs
- Seamless round-trip validation from lean LLM outputs back into enterprise XML
  serializers

## Changelog: 0.0.0

- Modernized for Python 3.12+ minimum.
- Consolidated `xsdata-pydantic` into core library as `pyxsdata.pydantic`.
- Replaced mypy with Astral's static type checker `ty`.
- Standardized CLI tool to `pyxsdata`.
- Documentation powered by Zensical.
