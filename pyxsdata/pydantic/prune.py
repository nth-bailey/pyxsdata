import copy
import fnmatch
import functools
import operator
from collections.abc import Sequence
from decimal import Decimal
from enum import Enum
from types import UnionType
from typing import Any, Literal, Union, get_args, get_origin

from pydantic import BaseModel, create_model
from pydantic_core import PydanticUndefined

from pyxsdata.models.datatype import (
    XmlDate,
    XmlDateTime,
    XmlDuration,
    XmlPeriod,
    XmlTime,
)


def _is_empty(val: Any) -> bool:
    """Return whether value is an empty collection."""
    return val is None or (isinstance(val, (list, tuple, set, dict)) and len(val) == 0)


def _to_json_leaf(val: Any) -> Any:
    """Convert leaf value to JSON-safe representation."""
    if isinstance(val, Enum):
        return val.value
    if isinstance(val, Decimal):
        return float(val)
    if hasattr(val, "isoformat") and callable(val.isoformat):
        return val.isoformat()
    return val


def _match_pattern(name: str, pattern: str) -> bool:
    """Match a field name or path against a glob pattern case-insensitively."""
    return fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(
        name.lower(), pattern.lower()
    )


def _matches_any(name: str, full_path: str, patterns: Sequence[str] | set[str]) -> bool:
    """Check if either the field name or full dot-path matches any pattern."""
    for pat in patterns:
        if _match_pattern(name, pat) or _match_pattern(full_path, pat):
            return True
        norm_pat = pat.replace(".*.", ".")
        if _match_pattern(full_path, norm_pat):
            return True
    return False


def _has_child_include(
    name: str,
    full_path: str,
    includes: Sequence[str] | set[str],
) -> bool:
    """Check if any include pattern targets children of this path."""
    for inc in includes:
        norm_inc = inc.replace(".*.", ".")
        if norm_inc.startswith("*"):
            return True
        if norm_inc.startswith(f"{name}.") or norm_inc.startswith(f"{full_path}."):
            return True
    return False


def _is_model_container(val: Any) -> bool:
    """Return whether value is a model or container of models."""
    if isinstance(val, (BaseModel, dict)):
        return True
    if isinstance(val, (list, tuple)) and not isinstance(
        val, (XmlDate, XmlDateTime, XmlTime, XmlDuration, XmlPeriod)
    ):
        return any(isinstance(x, (BaseModel, dict)) for x in val)
    return False


def prune_dump(
    obj: Any,
    *,
    include: Sequence[str] | set[str] | None = None,
    exclude: Sequence[str] | set[str] | None = None,
    exclude_namespaces: Sequence[str] | set[str] | None = None,
    exclude_prefixes: Sequence[str] | set[str] | None = None,
    exclude_none: bool = True,
    exclude_empty: bool = True,
    exclude_defaults: bool = False,
    max_depth: int | None = None,
    key_style: Literal["python", "xml", "prefixed_xml"] = "python",
    ns_map: dict[str, str] | None = None,
) -> Any:
    """Prune and serialize a Pydantic model tree into token-efficient JSON.

    Designed for sending XML-bound data models to LLMs and AI frameworks without
    token bloat, empty collections, or namespace noise.

    Args:
        obj: The Pydantic model instance, list, or mapping to prune.
        include: Field names or glob dot-paths to retain (e.g. `["id", "items.*"]`).
        exclude: Field names or glob dot-paths to drop (e.g. `["*.signature"]`).
        exclude_namespaces: XML namespace URIs to drop globally across the tree.
        exclude_prefixes: XML prefixes to drop globally across the tree.
        exclude_none: Whether to omit `None` values (defaults to True).
        exclude_empty: Whether to omit empty lists, sets, and dicts (True).
        exclude_defaults: Whether to omit fields whose value matches their default.
        max_depth: Truncate nesting deeper than this limit.
        key_style: Key naming format ("python", "xml", or "prefixed_xml").
        ns_map: Optional prefix-to-URI mapping for namespace resolution.

    Returns:
        A cleaned, token-efficient JSON-compatible dictionary or list.
    """
    ex_ns = set(exclude_namespaces) if exclude_namespaces else set()
    ex_pre = set(exclude_prefixes) if exclude_prefixes else set()
    inc_set = set(include) if include else None
    exc_set = set(exclude) if exclude else None

    uri_to_prefix = {v: k for k, v in ns_map.items()} if ns_map else {}

    def _prune_recursive(val: Any, current_path: str, depth: int) -> Any:
        if max_depth is not None and depth > max_depth:
            return None

        if isinstance(val, (XmlDate, XmlDateTime, XmlTime, XmlDuration, XmlPeriod)):
            return str(val)

        if isinstance(val, BaseModel):
            result: dict[str, Any] = {}
            for field_name, info in type(val).model_fields.items():
                field_val = getattr(val, field_name)

                if exclude_none and field_val is None:
                    continue

                if (
                    exclude_defaults
                    and info.default is not PydanticUndefined
                    and field_val == info.default
                ):
                    continue

                # Inspect XML metadata
                raw_meta = (
                    getattr(info, "xsdata_metadata", None)
                    or getattr(info, "json_schema_extra", None)
                    or {}
                )
                meta = raw_meta if isinstance(raw_meta, dict) else {}
                field_ns = meta.get("namespace")
                raw_xml_name = meta.get("name") or field_name

                # Check namespace exclusions
                if field_ns and field_ns in ex_ns:
                    continue

                # Check prefix exclusions
                xml_prefix = ""
                xml_local_name = raw_xml_name
                if ":" in raw_xml_name:
                    xml_prefix, xml_local_name = raw_xml_name.split(":", 1)
                elif field_ns and field_ns in uri_to_prefix:
                    xml_prefix = uri_to_prefix[field_ns]

                if xml_prefix and xml_prefix in ex_pre:
                    continue

                # Build dot-paths for checking
                path_py = f"{current_path}.{field_name}" if current_path else field_name
                path_xml = (
                    f"{current_path}.{xml_local_name}"
                    if current_path
                    else xml_local_name
                )
                prefixed_xml_name = (
                    f"{xml_prefix}:{xml_local_name}" if xml_prefix else xml_local_name
                )
                path_prefixed = (
                    f"{current_path}.{prefixed_xml_name}"
                    if current_path
                    else prefixed_xml_name
                )

                # Check exclusions
                if exc_set and (
                    _matches_any(field_name, path_py, exc_set)
                    or _matches_any(xml_local_name, path_xml, exc_set)
                    or _matches_any(prefixed_xml_name, path_prefixed, exc_set)
                ):
                    continue

                # Check inclusions
                if inc_set:
                    direct_match = (
                        _matches_any(field_name, path_py, inc_set)
                        or _matches_any(xml_local_name, path_xml, inc_set)
                        or _matches_any(prefixed_xml_name, path_prefixed, inc_set)
                    )
                    is_container = _is_model_container(field_val)
                    if is_container:
                        included = direct_match or (
                            _has_child_include(field_name, path_py, inc_set)
                            or _has_child_include(xml_local_name, path_xml, inc_set)
                            or _has_child_include(
                                prefixed_xml_name, path_prefixed, inc_set
                            )
                        )
                    else:
                        included = direct_match

                    if not included:
                        continue

                # Recurse
                pruned_child = _prune_recursive(field_val, path_py, depth + 1)

                if exclude_none and pruned_child is None:
                    continue
                if exclude_empty and _is_empty(pruned_child):
                    continue

                if key_style == "xml":
                    out_key = xml_local_name
                elif key_style == "prefixed_xml":
                    out_key = prefixed_xml_name
                else:
                    out_key = field_name

                result[out_key] = pruned_child

            return result

        if isinstance(val, (list, tuple)):
            res_list = []
            for item in val:
                pruned_item = _prune_recursive(item, current_path, depth)
                if exclude_none and pruned_item is None:
                    continue
                if exclude_empty and _is_empty(pruned_item):
                    continue
                res_list.append(pruned_item)
            return res_list

        if isinstance(val, dict):
            res_dict = {}
            for k, v in val.items():
                child_path = f"{current_path}.{k}" if current_path else str(k)
                pruned_val = _prune_recursive(v, child_path, depth + 1)
                if exclude_none and pruned_val is None:
                    continue
                if exclude_empty and _is_empty(pruned_val):
                    continue
                res_dict[k] = pruned_val
            return res_dict

        return _to_json_leaf(val)

    return _prune_recursive(obj, "", 0)


def _extract_model_type(type_hint: Any) -> type[BaseModel] | None:
    """Extract nested BaseModel type from a typing expression."""
    if isinstance(type_hint, type) and issubclass(type_hint, BaseModel):
        return type_hint
    origin = get_origin(type_hint)
    if origin is not None:
        for arg in get_args(type_hint):
            found = _extract_model_type(arg)
            if found is not None:
                return found
    return None


def _replace_model_type(
    type_hint: Any,
    old_cls: type[BaseModel],
    new_cls: type[BaseModel],
) -> Any:
    """Replace an old BaseModel class with a new projected BaseModel class."""
    if type_hint is old_cls:
        return new_cls
    origin = get_origin(type_hint)
    if origin is None:
        return type_hint
    new_args = tuple(
        _replace_model_type(arg, old_cls, new_cls) for arg in get_args(type_hint)
    )
    if origin in (UnionType, Union):
        return functools.reduce(operator.or_, new_args)
    return origin[new_args]


def project_model[T: BaseModel](
    model_cls: type[T],
    *,
    include: Sequence[str] | set[str],
    name: str | None = None,
) -> type[BaseModel]:
    """Dynamically project a lightweight Pydantic v2 sub-model from a complex schema.

    Creates a lean Pydantic model containing only the requested fields and nested
    sub-models, preserving validation rules (ge, le, pattern, etc.) and type hints.
    Ideal for LLM Structured Outputs (`response_format`) to avoid JSON schema bloat.

    Args:
        model_cls: The full Pydantic model class to project from.
        include: Set or sequence of field names or dot-paths to retain.
        name: Custom name for the projected model (defaults to `Projected<Original>`).

    Returns:
        A new Pydantic v2 `BaseModel` class containing only the selected fields.
    """
    normalized_includes = {p.replace(".*.", ".") for p in include}

    direct_fields: set[str] = set()
    nested_includes: dict[str, set[str]] = {}

    for path in normalized_includes:
        if "." in path:
            head, tail = path.split(".", 1)
            nested_includes.setdefault(head, set()).add(tail)
        else:
            direct_fields.add(path)

    projected_fields: dict[str, Any] = {}

    for field_name, info in model_cls.model_fields.items():
        raw_meta = (
            getattr(info, "xsdata_metadata", None)
            or getattr(info, "json_schema_extra", None)
            or {}
        )
        meta = raw_meta if isinstance(raw_meta, dict) else {}
        xml_name = meta.get("name") or field_name
        local_xml_name = xml_name.split(":", 1)[-1]

        matched_key = None
        for candidate in (field_name, xml_name, local_xml_name):
            if candidate in direct_fields or candidate in nested_includes:
                matched_key = candidate
                break

        if not matched_key:
            continue

        field_info_copy = copy.copy(info)
        annotation = info.annotation

        child_paths = nested_includes.get(matched_key)
        child_model = _extract_model_type(annotation)

        if child_paths and child_model:
            projected_child = project_model(
                child_model,
                include=child_paths,
                name=f"Projected{child_model.__name__}",
            )
            new_annotation = _replace_model_type(
                annotation, child_model, projected_child
            )
            projected_fields[field_name] = (new_annotation, field_info_copy)
        else:
            projected_fields[field_name] = (annotation, field_info_copy)

    if not projected_fields:
        raise ValueError(
            f"None of the include paths {include} matched fields on "
            f"{model_cls.__name__}"
        )

    model_name = name or f"Projected{model_cls.__name__}"
    return create_model(
        model_name,
        __base__=BaseModel,
        __config__=model_cls.model_config,
        __doc__=model_cls.__doc__,
        **projected_fields,
    )
