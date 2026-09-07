# Migrating from xsdata

`pyxsdata` is the modernized, actively maintained successor to
[`xsdata`](https://github.com/tefra/xsdata). It unifies formerly fragmented plugins
(such as `xsdata-pydantic`) into a single high-performance library built exclusively for
Python 3.12+.

If you are upgrading an existing project from `xsdata`, this guide highlights key
differences and provides a step-by-step checklist.

---

## Key Architectural Differences

| Feature                 | Legacy `xsdata`                                  | `pyxsdata`                                           |
| :---------------------- | :----------------------------------------------- | :--------------------------------------------------- |
| **Supported Python**    | Python 3.8 – 3.12                                | **Python 3.12+ exclusively**                         |
| **CLI Command**         | `xsdata`                                         | **Strictly `pyxsdata`**                              |
| **Pydantic Support**    | External plugin (`xsdata-pydantic`)              | **Built-in (`pyxsdata.pydantic`)**                   |
| **Dataclass Semantics** | Positional defaults (optional workarounds)       | **Native `kw_only=True` everywhere**                 |
| **Type Annotations**    | `typing.Union`, `typing.Optional`, `typing.List` | **`X \| Y`, `list[T]`, PEP 695 Generics**            |
| **Code Formatting**     | Unformatted or black                             | **Astral Ruff (`ruff>=0.9.8`)**                      |
| **XML Parser Engines**  | `xml.etree`, `lxml`                              | **`xml.etree`, `lxml`, and C++ `pugixml`**           |
| **Performance**         | Baseline xsdata                                  | **Up to 54% faster deserialization (2x throughput)** |
| **Type Checking**       | mypy                                             | **Astral `ty` with zero diagnostics**                |

---

## Migration Checklist

### 1. Update Dependencies

Remove `xsdata` and `xsdata-pydantic` from your `pyproject.toml` or `requirements.txt`,
and replace them with `pyxsdata`:

=== "Using uv"

    ```console
    $ uv remove xsdata xsdata-pydantic
    $ uv add "pyxsdata[cli,pydantic]"
    ```

=== "Using pip"

    ```console
    $ pip uninstall xsdata xsdata-pydantic
    $ pip install "pyxsdata[cli,pydantic]"
    ```

### 2. Update Import Statements

Replace all references to the `xsdata` namespace with `pyxsdata`:

```python
# Before
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata_pydantic.bindings import XmlParser as PydanticXmlParser

# After
from pyxsdata.formats.dataclass.parsers import XmlParser
from pyxsdata.formats.dataclass.serializers import XmlSerializer
from pyxsdata.pydantic.bindings import XmlParser as PydanticXmlParser
```

### 3. Update CLI Commands

The CLI command is strictly `pyxsdata`:

```console
# Before
$ xsdata generate schema.xsd --output pydantic

# After
$ pyxsdata generate schema.xsd --output pydantic
```

!!! note "Zero Backwards Compatibility Shims" `pyxsdata` intentionally does **not**
install an `xsdata` executable alias to ensure clear separation and prevent ambiguous
behavior in multi-package environments.

### 4. Benefit from Python 3.12+ `kw_only=True`

In older versions of `xsdata`, if a required XML element followed an optional element,
Python's `@dataclass` would raise a
`TypeError: non-default argument follows default argument`. Older solutions forced
non-nullable fields to be typed as `Optional[T] = None`.

In `pyxsdata`, all generated dataclasses use `kw_only=True` by default:

```python
@dataclass(kw_only=True)
class Person:
    middle_name: str | None = None  # optional with default
    last_name: str                  # required non-default field works cleanly!
```

This guarantees that required schema elements remain strictly required in Python.

### 5. Take Advantage of pugixml

If you parse large XML feeds or high-throughput API responses, install the `pugixml`
extra:

```console
$ uv add "pyxsdata[pugixml]"
```

And switch your parser handler:

```python
from pyxsdata.formats.dataclass.parsers import XmlParser
from pyxsdata.formats.dataclass.parsers.handlers import PugixmlEventHandler

parser = XmlParser(handler=PugixmlEventHandler)
data = parser.parse("huge_feed.xml", FeedModel)
```

Read more in the [Parser Backends Guide](data_binding/backends.md).

### 6. Faster Deserialization Out of the Box

`pyxsdata` includes built-in optimizations that make XML deserialization up to **54%
faster** (over **2x throughput**) than legacy `xsdata`:

- **Direct Scalar Type Fast-Paths**: Bypasses general converter dispatch and exception
  handling for single `str`, `int`, and `float` candidate types, accelerating primitive
  scalar conversions by up to 2.7x.
- **ProxyConverter Fast-Path**: Calls target factory callables directly for `XmlDate`,
  `XmlTime`, `XmlDateTime`, `XmlDuration`, and `XmlPeriod` without allocating keyword
  argument dictionaries.
- **Cached Schema Metadata & Tuple Iteration**: Caches `XmlMeta.get_children` resolution
  as immutable tuples, eliminating hundreds of thousands of generator allocations and
  `iter()` call overheads.
- **Fast-Path Primitive Node Instantiation**: Immediately constructs `PrimitiveNode` for
  scalar fields without querying XSI attributes or factory classes.
- **Static Method Binding**: Uses static methods for field binding to avoid per-call
  bound method descriptor construction.
- **Slice-Free Intermediate Object Processing**: Traverses queued object tuples using
  direct indexing instead of allocating intermediate sublists during object binding.
- **Zero-Cost Converter Dispatch & Single-Type Fast-Path**: Replaced expensive
  exception-suppression wrappers with direct dictionary lookups.
- **MRO Converter Caching**: Fast-paths class inheritance lookups by caching converter
  resolution directly in the type registry.
- **Parser Node Caching**: Avoids repeated module imports in parsing hot paths.
- **Short-Circuited XSI Attribute Checks**: Instantly skips XSI type and nil checks when
  elements carry no attributes.
