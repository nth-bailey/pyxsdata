import random
import tempfile
from pathlib import Path
from unittest import mock

from pyxsdata.codegen.exceptions import CodegenError
from pyxsdata.codegen.resolver import DependenciesResolver
from pyxsdata.formats.dataclass.generator import DataclassGenerator
from pyxsdata.models.config import GeneratorConfig
from pyxsdata.utils.testing import ClassFactory, FactoryTestCase


class DataclassGeneratorTests(FactoryTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.maxDiff = None
        config = GeneratorConfig()
        self.generator = DataclassGenerator(config)

    @mock.patch.object(DataclassGenerator, "ruff_code")
    @mock.patch.object(DataclassGenerator, "validate_imports")
    @mock.patch.object(DataclassGenerator, "render_package")
    @mock.patch.object(DataclassGenerator, "render_module")
    def test_render(
        self,
        mock_render_module,
        mock_render_package,
        mock_validate_imports,
        mock_ruff_code,
    ) -> None:
        classes = [
            ClassFactory.create(package="foo.bar", module="tests"),
            ClassFactory.create(package="bar.foo", module="tests"),
            ClassFactory.create(package="thug.life", module="tests"),
        ]

        mock_render_module.return_value = "module"
        mock_render_package.return_value = "package"

        iterator = self.generator.render(classes)

        cwd = Path.cwd()
        actual = [(out.path, out.title, out.source) for out in iterator]
        expected = [
            (cwd.joinpath("foo/bar/__init__.py"), "init", "package"),
            (cwd.joinpath("foo/__init__.py"), "init", "# nothing here\n"),
            (cwd.joinpath("bar/foo/__init__.py"), "init", "package"),
            (cwd.joinpath("bar/__init__.py"), "init", "# nothing here\n"),
            (cwd.joinpath("thug/life/__init__.py"), "init", "package"),
            (cwd.joinpath("thug/__init__.py"), "init", "# nothing here\n"),
            (cwd.joinpath("foo/bar/tests.py"), "foo.bar.tests", "module"),
            (cwd.joinpath("bar/foo/tests.py"), "bar.foo.tests", "module"),
            (cwd.joinpath("thug/life/tests.py"), "thug.life.tests", "module"),
        ]
        self.assertEqual(expected, actual)
        mock_render_package.assert_has_calls(
            [
                mock.call([classes[0]], "foo.bar"),
                mock.call([classes[1]], "bar.foo"),
                mock.call([classes[2]], "thug.life"),
            ]
        )
        mock_render_module.assert_has_calls([mock.call(mock.ANY, [x]) for x in classes])
        mock_validate_imports.assert_called_once()

    def test_render_package(self) -> None:
        classes = [
            ClassFactory.create(qname="a", package="foo", module="tests"),
            ClassFactory.create(qname="b", package="foo", module="tests"),
            ClassFactory.create(qname="c", package="foo", module="tests"),
            ClassFactory.create(qname="a", package="foo", module="bar"),
        ]

        random.shuffle(classes)

        actual = self.generator.render_package(classes, "foo.tests")
        expected = (
            "from foo.bar import A as BarA\n"
            "from foo.tests import (\n"
            "    A as TestsA,\n"
            "    B,\n"
            "    C,\n"
            ")\n"
            "\n"
            "__all__ = [\n"
            '    "BarA",\n'
            '    "TestsA",\n'
            '    "B",\n'
            '    "C",\n'
            "]"
        )
        self.assertEqual(expected, actual)

    def test_render_package_lazy_load(self) -> None:
        self.generator.config.output.lazy_load = True
        classes = [
            ClassFactory.create(qname="a", package="foo", module="tests"),
            ClassFactory.create(qname="b", package="foo", module="tests"),
            ClassFactory.create(qname="c", package="foo", module="tests"),
            ClassFactory.create(qname="a", package="foo", module="bar"),
        ]

        random.shuffle(classes)

        actual = self.generator.render_package(classes, "foo.tests")
        self.assertIn("import importlib", actual)
        self.assertIn("def __getattr__(name: str):", actual)
        self.assertIn("def __dir__():", actual)
        self.assertIn("_LAZY_MODULES: dict[str, str] = {", actual)
        self.assertIn('"BarA": "foo.bar"', actual)
        self.assertIn('"TestsA": "foo.tests"', actual)
        self.assertIn('"B": "foo.tests"', actual)
        self.assertIn('"C": "foo.tests"', actual)
        self.assertIn(
            '__all__ = [\n    "BarA",\n    "TestsA",\n    "B",\n    "C",\n]', actual
        )
        # Reset for subsequent tests
        self.generator.config.output.lazy_load = False

    def test_lazy_load_runtime_execution(self) -> None:
        import importlib
        import sys

        with tempfile.TemporaryDirectory() as tmpdir:
            pkg_dir = Path(tmpdir).joinpath("lazy_sample_pkg")
            pkg_dir.mkdir(parents=True, exist_ok=True)

            sub_file = pkg_dir.joinpath("sub.py")
            sub_file.write_text("class MyLazyClass:\n    pass\n", encoding="utf-8")

            classes = [
                ClassFactory.create(
                    qname="MyLazyClass", package="lazy_sample_pkg", module="sub"
                )
            ]
            self.generator.config.output.lazy_load = True
            init_code = self.generator.render_package(classes, "lazy_sample_pkg")
            self.generator.config.output.lazy_load = False

            init_file = pkg_dir.joinpath("__init__.py")
            init_file.write_text(init_code, encoding="utf-8")

            sys.path.insert(0, tmpdir)
            try:
                mod = importlib.import_module("lazy_sample_pkg")
                # sub is not in sys.modules yet
                self.assertNotIn("lazy_sample_pkg.sub", sys.modules)

                # Attribute access loads on demand
                cls = getattr(mod, "MyLazy" + "Class")
                self.assertEqual("MyLazyClass", cls.__name__)
                self.assertIn("lazy_sample_pkg.sub", sys.modules)

                # __dir__ returns __all__
                self.assertIn("MyLazyClass", dir(mod))

                # Non-existent attribute raises AttributeError
                with self.assertRaises(AttributeError):
                    _ = getattr(mod, "Non" + "Existent")
            finally:
                sys.path.remove(tmpdir)
                sys.modules.pop("lazy_sample_pkg", None)
                sys.modules.pop("lazy_sample_pkg.sub", None)

    def test_render_module(self) -> None:
        classes = [
            ClassFactory.enumeration(2, help="\n\nI am enum  "),
            ClassFactory.elements(2),
            ClassFactory.service(2),
        ]
        classes[0].attrs[0].help = "I am a member"
        classes[1].attrs[0].help = "I am a field"

        resolver = DependenciesResolver({})

        actual = self.generator.render_module(resolver, classes)
        expected = (
            "from __future__ import annotations\n"
            "from dataclasses import dataclass, field\n"
            "from enum import Enum\n"
            "\n"
            '__NAMESPACE__ = "pyxsdata"\n'
            "\n"
            "\n"
            "class ClassB(Enum):\n"
            '    """\n'
            "    I am enum.\n"
            "\n"
            "    :cvar ATTR_B: I am a member\n"
            "    :cvar ATTR_C:\n"
            '    """\n'
            "    ATTR_B = False\n"
            "    ATTR_C = False\n"
            "@dataclass(kw_only=True)\n"
            "class ClassC:\n"
            '    """\n'
            "    :ivar attr_d: I am a field\n"
            "    :ivar attr_e:\n"
            '    """\n'
            "    class Meta:\n"
            '        name = "class_C"\n'
            "\n"
            "    attr_d: str = field(\n"
            "        metadata={\n"
            '            "name": "attr_D",\n'
            '            "type": "Element",\n'
            "        }\n"
            "    )\n"
            "    attr_e: str = field(\n"
            "        metadata={\n"
            '            "name": "attr_E",\n'
            '            "type": "Element",\n'
            "        }\n"
            "    )\n"
            "class ClassD:\n"
            '    attr_f = "None"\n'
            '    attr_g = "None"'
        )

        self.assertEqual(expected, actual)

    def test_render_module_with_mixed_target_namespaces(self) -> None:
        classes = [
            ClassFactory.elements(1, qname="{foo}bar"),
            ClassFactory.elements(1, qname="{bar}foo"),
        ]
        resolver = DependenciesResolver({})

        actual = self.generator.render_module(resolver, classes)
        expected = (
            "from __future__ import annotations\n"
            "from dataclasses import dataclass, field\n"
            "\n"
            "\n"
            "@dataclass(kw_only=True)\n"
            "class Foo:\n"
            "    class Meta:\n"
            '        name = "foo"\n'
            '        target_namespace = "bar"\n'
            "\n"
            "    attr_c: str = field(\n"
            "        metadata={\n"
            '            "name": "attr_C",\n'
            '            "type": "Element",\n'
            "        }\n"
            "    )\n"
            "@dataclass(kw_only=True)\n"
            "class Bar:\n"
            "    class Meta:\n"
            '        name = "bar"\n'
            '        target_namespace = "foo"\n'
            "\n"
            "    attr_b: str = field(\n"
            "        metadata={\n"
            '            "name": "attr_B",\n'
            '            "type": "Element",\n'
            "        }\n"
            "    )"
        )

        self.assertEqual(expected, actual)

    def test_module_name(self) -> None:
        self.assertEqual("foo_bar", self.generator.module_name("fooBar"))
        self.assertEqual("foo_bar_wtf", self.generator.module_name("fooBar.wtf"))
        self.assertEqual("mod_1111", self.generator.module_name("1111"))
        self.assertEqual("xs_string", self.generator.module_name("xs:string"))
        self.assertEqual("foo_bar_bam", self.generator.module_name("foo:bar_bam"))
        self.assertEqual("bar_bam", self.generator.module_name("urn:bar_bam"))

    def test_package_name(self) -> None:
        self.assertEqual(
            "foo.bar_bar.pkg_1", self.generator.package_name("Foo.BAR_bar.1")
        )

        self.assertEqual("", self.generator.package_name(""))

    def test_ruff_code_with_invalid_code(self) -> None:
        src_code = (
            "class AlternativeText:\n"
            "    class Meta:\n"
            '        namespace = "pyxsdata"\n'
            "\n"
            "    foo: Optional[Union[]] = field(\n"
            "           init=False,\n"
            '           metadata={"type": "Ignore"}\n'
            "    )\n"
            "    bar: str\n"
            "    thug: str"
        )

        with tempfile.NamedTemporaryFile(delete=True, suffix=".py") as temp_file:
            temp_file.write(src_code.encode())
            temp_file.seek(0)

            with self.assertRaises(CodegenError):
                self.generator.ruff_code([temp_file.name])

    def test_render_str_enum(self) -> None:
        classes = [ClassFactory.enumeration(2, qname="MyEnum")]
        resolver = DependenciesResolver({})

        self.generator.config.output.str_enums = True
        actual = self.generator.render_module(resolver, classes)
        self.assertIn("from enum import StrEnum", actual)
        self.assertIn("class MyEnum(StrEnum):", actual)

        self.generator.config.output.str_enums = False
        actual = self.generator.render_module(resolver, classes)
        self.assertIn("from enum import Enum", actual)
        self.assertIn("class MyEnum(Enum):", actual)
