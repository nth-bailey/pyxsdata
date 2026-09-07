try:
    from pyxsdata.codegen.writer import CodeWriter
    from pyxsdata.pydantic.generator import PydanticGenerator

    CodeWriter.register_generator("pydantic", PydanticGenerator)
except ImportError:  # pragma: no cover
    pass
