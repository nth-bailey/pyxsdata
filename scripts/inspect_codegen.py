#!/usr/bin/env python3
"""Codegen AST & Template Inspector.

Parses an XSD/WSDL/DTD schema, runs the AST mapper, and displays the internal Class
metadata, attributes, extensions, and the rendered Python source code for inspection.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Ensure .venv/bin is in PATH for ruff and other tools
venv_bin = str(Path(__file__).resolve().parent.parent / ".venv" / "bin")
if venv_bin not in os.environ.get("PATH", ""):
    os.environ["PATH"] = f"{venv_bin}:{os.environ.get('PATH', '')}"

from pyxsdata.codegen.transformer import ResourceTransformer
from pyxsdata.formats.dataclass.generator import DataclassGenerator
from pyxsdata.models.config import GeneratorConfig, OutputFormat


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect schema AST and generated code.")
    parser.add_argument("schema", type=str, help="Path to schema file (XSD, WSDL, DTD).")
    parser.add_argument("class_name", nargs="?", default=None, help="Optional class name to filter.")
    parser.add_argument(
        "--format",
        choices=["dataclass", "pydantic"],
        default="dataclass",
        help="Target output format (default: dataclass).",
    )

    args = parser.parse_args()
    schema_path = Path(args.schema).resolve()

    if not schema_path.exists():
        print(f"Error: Schema file not found: {schema_path}", file=sys.stderr)
        sys.exit(1)

    config = GeneratorConfig()
    if args.format == "pydantic":
        config.output.format = OutputFormat.PYDANTIC

    transformer = ResourceTransformer(config)
    transformer.process([schema_path.as_uri()])
    classes = transformer.classes

    if args.class_name:
        matched = [c for c in classes if args.class_name.lower() in c.name.lower()]
    else:
        matched = classes

    if not matched:
        print(f"No classes found matching '{args.class_name}'.")
        sys.exit(1)

    generator = DataclassGenerator(config)
    generator.filters.set_classes(classes)

    for obj in matched:
        print("\n" + "=" * 80)
        print(f"Class: {obj.name} (QName: {obj.qname})")
        print("=" * 80)
        print(f"  • Tag: {obj.tag}")
        print(f"  • Local Type: {obj.local_type}")
        print(f"  • Target Namespace: {obj.target_namespace}")
        print(f"  • Meta Name: {obj.meta_name}")
        print(f"  • Nillable: {obj.is_nillable}")
        print(f"  • Has Meta: {generator.filters.class_has_meta(obj)}")

        if obj.extensions:
            print("  • Extensions:")
            for ext in obj.extensions:
                base_cls = generator.filters.classes_by_ref.get(
                    ext.type.reference
                ) or generator.filters.classes.get(ext.type.qname)
                base_has_meta = generator.filters.class_has_meta(base_cls) if base_cls else False
                print(f"    - Base: {ext.type.qname} (native={ext.type.native}, base_has_meta={base_has_meta})")
            meta_bases = generator.filters.class_meta_bases(obj, obj.name)
            print(f"  • Meta Bases: {meta_bases}")

        if obj.attrs:
            print(f"  • Attributes ({len(obj.attrs)}):")
            for attr in obj.attrs:
                type_names = [tp.qname for tp in attr.types]
                print(f"    - {attr.name}: {', '.join(type_names)} (tag={attr.tag})")

        print("\n--- Rendered Source Code ---")
        rendered = generator.render_classes([obj], module_namespace=obj.target_namespace)
        print(rendered.strip())


if __name__ == "__main__":
    main()
