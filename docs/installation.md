# Installation

## Using pip

```console
pip install "pyxsdata[cli,lxml,soap,pydantic]"
```

!!! hint

    - Install the `cli` requirements for the code generator
    - Install the `pydantic` requirements for Pydantic v2 model generation and data binding
    - Install the `soap` requirements for the builtin wsdl client
    - Install `lxml` for enhanced performance and advanced features
    - Install `pugixml` for ultra-fast C++ XML pull-parsing via pygixml

## From repository

```console
pip install "pyxsdata[cli,lxml,pugixml,pydantic] @ git+https://github.com/nth-bailey/pyxsdata"
```

## Verify installation

Verify installation using the cli entry point:

```console exec="1" source="console"
$ pyxsdata --help
```

## Requirements

!!! Note "pyxsdata relies on these awesome libraries and supports `python >= 3.12`"

    - [pydantic](https://docs.pydantic.dev/) - Data validation & settings management
    - [lxml](https://lxml.de/) - XML advanced features
    - [pygixml](https://github.com/vovcacik/pygixml) - High-performance pugixml streaming parser
    - [requests](https://requests.readthedocs.io/) - Webservice Default Transport
    - [click](https://click.palletsprojects.com/) - CLI entry point
    - [toposort](https://pypi.org/project/toposort/) - Resolve class ordering
    - [jinja2](https://jinja.palletsprojects.com/) - Code generation
    - [ruff](https://pypi.org/project/ruff/) - Code formatting
