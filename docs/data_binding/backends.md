# Parser Backends & Performance

`pyxsdata` features a modular, event-driven architecture that decouples XML parsing
events from Python model instantiation. This allows you to choose between multiple XML
parser backends depending on your performance, memory, and feature requirements.

---

## Overview of Backends

`pyxsdata` supports four primary XML deserialization options:

| Backend Handler           | Underlying Engine         | Extra Dependency    | Best For                                                           |
| :------------------------ | :------------------------ | :------------------ | :----------------------------------------------------------------- |
| **`CoreEventHandler`**    | Rust + PyO3 (`quick-xml`) | `pyxsdata[core]`    | **Ultra-fast throughput** (~290k objs/sec, 15x faster than legacy) |
| **`NativeEventHandler`**  | Python `xml.etree`        | _None (built-in)_   | Zero-dependency environments, AWS Lambda, lightweight scripts      |
| **`LxmlEventHandler`**    | C `libxml2` / `lxml`      | `pyxsdata[lxml]`    | DTD validation, XInclude, advanced entity resolution               |
| **`PugixmlEventHandler`** | C++ `pugixml` / `pygixml` | `pyxsdata[pugixml]` | High-frequency streaming API ingestion, low latency                |

---

## 1. Native Rust Core (`CoreEventHandler` / `CoreXmlParser`)

The `core` backend is powered by
[`pyxsdata-core`](https://github.com/nth-bailey/pyxsdata-core), a dedicated native
extension built with [PyO3](https://pyo3.rs) and
[`quick-xml`](https://github.com/tafia/quick-xml). It bypasses Python intermediate DOM
trees and event queues entirely, converting XML tokens directly into Python dataclass
models via C-API at **~290,000+ objects/sec**.

### When to Use

- Maximum possible ingestion speed (9.5x faster than pure Python, 15x faster than legacy
  `xsdata`).
- High-throughput message queues, large XML bulk imports, and real-time APIs.

### Installation & Usage

```console
$ uv add "pyxsdata[core]"
```

Use `CoreXmlParser` directly:

```python
from pyxsdata.formats.dataclass.parsers import CoreXmlParser
from myapp.models import Catalog

parser = CoreXmlParser()
catalog = parser.parse("catalog.xml", Catalog)
```

Or pass `handler=CoreEventHandler` to `XmlParser`:

```python
from pyxsdata.formats.dataclass.parsers import XmlParser
from pyxsdata.formats.dataclass.parsers.handlers import CoreEventHandler
from myapp.models import Catalog

parser = XmlParser(handler=CoreEventHandler)
catalog = parser.parse("catalog.xml", Catalog)
```

---

## 2. Pugixml Backend (`PugixmlEventHandler`)

The `pugixml` backend is powered by [`pygixml`](https://github.com/vovcacik/pygixml), a
high-speed Cython wrapper around the battle-tested C++ [pugixml](https://pugixml.org/)
library combined with yxml.

### When to Use

- High-throughput XML processing (e.g. consuming high-rate XML message queues or
  webhooks).
- Large XML files where parsing speed and CPU utilization are critical.
- Microservices seeking lowest request latency.

### Installation & Usage

```console
$ uv add "pyxsdata[pugixml]"
```

Pass `handler=PugixmlEventHandler` to the parser:

```python
from pyxsdata.formats.dataclass.parsers import XmlParser
from pyxsdata.formats.dataclass.parsers.handlers import PugixmlEventHandler
from myapp.models import Catalog

# Use pugixml streaming parser
parser = XmlParser(handler=PugixmlEventHandler)
catalog = parser.parse("catalog.xml", Catalog)
```

Works identically with Pydantic v2:

```python
from pyxsdata.pydantic.bindings import XmlParser
from pyxsdata.formats.dataclass.parsers.handlers import PugixmlEventHandler
from myapp.models import Catalog

parser = XmlParser(handler=PugixmlEventHandler)
catalog = parser.parse("catalog.xml", Catalog)
```

---

## 2. lxml Backend (`LxmlEventHandler`)

The `lxml` backend is powered by Python's popular `lxml` package wrapping C `libxml2`.

### When to Use

- You need DTD resolution or DTD validation (`load_dtd=True`).
- You need XInclude processing (`process_xinclude=True`).
- You want to parse directly from existing `lxml.etree.Element` or `ElementTree`
  objects.

### Installation & Usage

```console
$ uv add "pyxsdata[lxml]"
```

```python
from pyxsdata.formats.dataclass.parsers import XmlParser
from pyxsdata.formats.dataclass.parsers.config import ParserConfig
from pyxsdata.formats.dataclass.parsers.handlers import LxmlEventHandler
from myapp.models import Catalog

config = ParserConfig(process_xinclude=True, load_dtd=True)
parser = XmlParser(config=config, handler=LxmlEventHandler)
catalog = parser.parse("catalog.xml", Catalog)
```

---

## 3. Standard Library Backend (`NativeEventHandler`)

The standard library backend uses Python's built-in `xml.etree.ElementTree.iterparse`.

### When to Use

- Minimal container images or edge environments where installing C/C++ extensions is
  prohibited or difficult.
- Standard workloads where XML documents are small to moderate in size.
- Zero-dependency deployments.

### Usage

The native handler is the default fallback when neither `lxml` nor `pygixml` is
explicitly requested:

```python
from pyxsdata.formats.dataclass.parsers import XmlParser
from pyxsdata.formats.dataclass.parsers.handlers import NativeEventHandler
from myapp.models import Catalog

parser = XmlParser(handler=NativeEventHandler)
catalog = parser.parse("catalog.xml", Catalog)
```

---

## Performance Comparison & Recommendations

### General Guidelines

1. **For Maximum Ingestion Speed**: Use `PugixmlEventHandler`. Its C++ pull parser
   yields the lowest overhead when reading XML files.
2. **For Advanced XML Specs**: Use `LxmlEventHandler` if your schemas require external
   DTDs or XInclude resolution.
3. **For Zero Dependencies**: Use `NativeEventHandler`.

### Performance vs Legacy xsdata

Through hot-path optimizations in metadata lookup caching, primitive node fast paths,
converter dispatch, and parser event handlers, `pyxsdata` deserializes XML significantly
faster than legacy `xsdata`:

| Backend Handler           | Legacy `xsdata` | `pyxsdata`  | Speedup             |
| :------------------------ | :-------------- | :---------- | :------------------ |
| **`CoreEventHandler`**    | ~513.0 ms       | **34.4 ms** | **~15.0x (1,490%)** |
| **`NativeEventHandler`**  | 728.9 ms        | 332.5 ms    | **+54.4% (2.2x)**   |
| **`LxmlEventHandler`**    | 753.2 ms        | 375.2 ms    | **+50.2% (2.0x)**   |
| **`PugixmlEventHandler`** | 883.8 ms        | 509.4 ms    | **+42.4% (1.7x)**   |

_(Benchmark: 10,000 complex XML items parsed into dataclasses, lowest of 5 runs)_

### Thread Safety & Context Reuse

Creating an `XmlContext` inspects Python model classes and builds metadata caches. For
optimal performance across all handlers:

```python
from pyxsdata.formats.dataclass.context import XmlContext
from pyxsdata.formats.dataclass.parsers import XmlParser

# Create context once and reuse across threads/workers
shared_context = XmlContext()

# Initialize parsers reusing the cache
parser = XmlParser(context=shared_context)
```
