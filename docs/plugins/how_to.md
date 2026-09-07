# How to extend xsdata

There are two main entrypoints that developers can leverage to add support a new
generator output or/and a new class type for data bindings.

## `xsdata.plugins.cli`

This entrypoint allows developers to register a new
[pyxsdata.formats.mixins.AbstractGenerator][].

```python
from pyxsdata.codegen.writer import CodeWriter
from pyxsdata.formats.mixins import AbstractGenerator

class AwesomeGenerator(AbstractGenerator):
    ...

CodeWriter.register_generator("awesome", AwesomeGenerator)
```

Which can be used during code generation.

```console
$ pyxsdata generate --output awesome
```

## `xsdata.plugins.class_types`

This entrypoint can be used to register a new
[pyxsdata.formats.dataclass.compat.ClassType][] for binding operations.

```python
from pyxsdata.formats.dataclass.compat import class_types
from pyxsdata.formats.dataclass.compat import ClassType

class AwesomeType(ClassType):
    ...

class_types.register("awesome", AwesomeType())
```

Which then can be used like this:

```python
from pyxsdata.formats.dataclass.context import XmlContext
from pyxsdata.formats.dataclass.parsers import XmlParser

context = XmlContext(class_types="awesome")
parser = XmlParser(context=context)
```
