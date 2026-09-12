# pyxsdata AI Agent Guide

Quick-reference instructions for AI coding assistants (Claude, Cursor, Copilot,
Antigravity, etc.) using `pyxsdata` in Python projects.

---

## 1. Core Architectural Rules & Invariants

1. **Strictly `pyxsdata` CLI (No Backwards Compatibility Shims)**:
   - Always run the CLI as `pyxsdata`, never `xsdata`.
   - Do NOT suggest installing or using `xsdata` or `xsdata-pydantic`.

2. **Native Pydantic v2 Integration (`pyxsdata.pydantic`)**:
   - Pydantic v2 is natively supported under `pyxsdata.pydantic`.
   - For Pydantic models, use
     `from pyxsdata.pydantic.bindings import XmlParser, XmlSerializer`.

3. **Modern Python 3.12+ Exclusively**:
   - Uses PEP 695 generics, `X | None` union syntax, and `kw_only` dataclasses.

---

## 2. Common Recipes

### A. Parse XML into Dataclasses

```python
from pyxsdata.formats.dataclass.parsers import XmlParser

parser = XmlParser()

# From string:
instance = parser.from_string("<User><name>Alice</name></User>", User)

# From file path:
from pathlib import Path

instance = parser.from_path(Path("data.xml"), User)

# From stream/bytes:
import io

instance = parser.parse(io.BytesIO(b"..."), User)
```

### B. Serialize Dataclasses to XML

```python
from pyxsdata.formats.dataclass.serializers import XmlSerializer
from pyxsdata.formats.dataclass.serializers.config import SerializerConfig

# Optional pretty-printing and XML declaration
config = SerializerConfig(pretty_print=True, xml_declaration=True)
serializer = XmlSerializer(config=config)

xml_output = serializer.render(instance)
```

### C. Pydantic v2 Models

```python
from pyxsdata.pydantic.bindings import XmlParser, XmlSerializer

parser = XmlParser()
model_instance = parser.from_string(xml_str, MyPydanticModel)

serializer = XmlSerializer()
xml_str = serializer.render(model_instance)
```

### D. Code Generation CLI

```bash
# Generate standard Python dataclasses from XSD
pyxsdata generate schema.xsd --output dataclasses

# Generate Pydantic v2 models from XSD
pyxsdata generate schema.xsd --output pydantic

# Generate models from XML document
pyxsdata generate document.xml --output dataclasses
```

---

## 3. Common Pitfalls & Quick Fixes

- **Pitfall**: Attempting `from xsdata... import ...` **Fix**: Replace with
  `from pyxsdata... import ...`.
- **Pitfall**: Attempting `from xsdata_pydantic import ...` **Fix**: Replace with
  `from pyxsdata.pydantic.bindings import XmlParser, XmlSerializer`.
- **Pitfall**: Passing raw XML string into `parser.parse(...)` **Fix**: Use
  `parser.from_string(xml_text, TargetClass)` for strings, or
  `parser.from_path(path, TargetClass)` for files.
