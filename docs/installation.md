# Installation Guide

`pyxsdata` requires **Python 3.12+** and is available as a pre-built wheel on
[PyPI](https://pypi.org/project/pyxsdata/).

---

## Quick Install

=== "Using uv (Recommended)"

    ```console
    # Recommended setup with CLI, Pydantic v2, and pugixml
    $ uv add "pyxsdata[cli,pydantic,pugixml]"

    # Or install everything
    $ uv add "pyxsdata[all]"
    ```

=== "Using pip"

    ```console
    # Recommended setup
    $ pip install "pyxsdata[cli,pydantic,pugixml]"

    # Or install everything
    $ pip install "pyxsdata[all]"
    ```

=== "Using Poetry"

    ```console
    $ poetry add "pyxsdata[cli,pydantic,pugixml]"
    ```

---

## Optional Dependency Extras

`pyxsdata` is modular so you only install what your application requires:

| Extra          | Description                                                                   | When to Include                                                    |
| :------------- | :---------------------------------------------------------------------------- | :----------------------------------------------------------------- |
| **`cli`**      | Code generator command-line interface (`click`, `jinja2`, `toposort`, `ruff`) | Whenever generating Python models from schemas or documents        |
| **`pydantic`** | Native Pydantic v2 support (`pydantic>=2.10.0`)                               | To generate Pydantic models and use `pyxsdata.pydantic.bindings`   |
| **`pugixml`**  | C++ `pugixml` fast pull parser (`pygixml>=0.12.0`)                            | For high-throughput XML parsing and lowest latency                 |
| **`lxml`**     | C `libxml2` binding (`lxml>=5.3.0`)                                           | For DTD loading, XInclude processing, or parsing from `lxml` trees |
| **`soap`**     | SOAP web services client transport (`requests>=2.32.3`)                       | When consuming SOAP/WSDL web services                              |
| **`all`**      | Installs all of the above extras                                              | For full local development and testing                             |

---

## Installing from Git Repository

To install the latest unreleased development build directly from GitHub:

=== "Using uv"

    ```console
    $ uv add "pyxsdata[all] @ git+https://github.com/nth-bailey/pyxsdata"
    ```

=== "Using pip"

    ```console
    $ pip install "pyxsdata[all] @ git+https://github.com/nth-bailey/pyxsdata"
    ```

---

## Verify Your Installation

Check that the CLI is installed and accessible:

```console exec="1" source="console"
$ pyxsdata --help
```

In Python, verify the package and version:

```python
import pyxsdata

print(pyxsdata.__version__)
```
