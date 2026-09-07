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

## From repository

```console
pip install "pyxsdata[cli,lxml,pydantic] @ git+https://github.com/nth-bailey/pyxsdata"
```

## Verify installation

Verify installation using the cli entry point:

```console exec="1" source="console"
$ pypyxsdata --help
```

## Requirements

!!! Note "pyxsdata relies on these awesome libraries and supports `python >= 3.12`"

    - [pydantic](https://docs.pydantic.dev/) - Data validation & settings management
    - [lxml](https://lxml.de/) - XML advanced features
    - [requests](https://requests.readthedocs.io/) - Webservice Default Transport
    - [click](https://click.palletsprojects.com/) - CLI entry point
    - [toposort](https://pypi.org/project/toposort/) - Resolve class ordering
    - [jinja2](https://jinja.palletsprojects.com/) - Code generation
    - [ruff](https://pypi.org/project/ruff/) - Code formatting
