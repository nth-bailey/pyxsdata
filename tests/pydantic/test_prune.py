from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field
import pytest

from pyxsdata.models.datatype import XmlDate
from pyxsdata.pydantic import project_model, prune_dump
from pyxsdata.pydantic.fields import field


class StatusEnum(str, Enum):
    ACTIVE = "active"
    PENDING = "pending"


class AuditInfo(BaseModel):
    created_by: str = field(metadata={"name": "CreatedBy", "type": "Element"})
    signature: str = field(
        metadata={
            "name": "ds:Signature",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
            "type": "Element",
        }
    )


class Item(BaseModel):
    sku: str = field(metadata={"name": "SKU", "type": "Element"})
    price: float = Field(..., ge=0.0, description="Item price")
    quantity: int = Field(default=1, ge=1)
    notes: list[str] = Field(default_factory=list)
    ext_data: str | None = field(
        default=None,
        metadata={
            "name": "ext:Extension",
            "namespace": "urn:oasis:names:extension",
            "type": "Element",
        },
    )


class Customer(BaseModel):
    name: str = field(metadata={"name": "Name", "type": "Element"})
    email: str = field(metadata={"name": "Email", "type": "Element"})
    secret_token: str = field(default="secret-123")


class Order(BaseModel):
    id: str = field(
        metadata={
            "name": "ID",
            "namespace": "urn:enterprise:order",
            "type": "Element",
        }
    )
    status: StatusEnum = StatusEnum.ACTIVE
    order_date: XmlDate = field(
        default_factory=lambda: XmlDate(2026, 9, 13),
        metadata={"name": "OrderDate", "type": "Element"},
    )
    total: Decimal = Decimal("99.95")
    customer: Customer
    items: list[Item] = Field(default_factory=list)
    audit: AuditInfo | None = None
    tags: list[str] = Field(default_factory=list)
    empty_dict: dict[str, str] = Field(default_factory=dict)


@pytest.fixture
def sample_order() -> Order:
    return Order(
        id="ORD-001",
        status=StatusEnum.ACTIVE,
        order_date=XmlDate(2026, 9, 13),
        total=Decimal("150.50"),
        customer=Customer(name="Alice Corp", email="alice@example.com"),
        items=[
            Item(sku="SKU-A", price=50.0, quantity=2, notes=["urgent"]),
            Item(sku="SKU-B", price=25.25, quantity=2, ext_data="extra"),
        ],
        audit=AuditInfo(
            created_by="system",
            signature="xyz123crypto",
        ),
        tags=[],
        empty_dict={},
    )


def test_prune_dump_defaults_and_token_reducers(sample_order: Order):
    # Default prune_dump excludes None and empty collections
    result = prune_dump(sample_order)

    assert result["id"] == "ORD-001"
    assert result["status"] == "active"
    assert result["order_date"] == "2026-09-13"
    assert result["total"] == 150.50
    assert result["customer"]["name"] == "Alice Corp"
    assert len(result["items"]) == 2
    assert "tags" not in result  # empty list stripped
    assert "empty_dict" not in result  # empty dict stripped


def test_prune_dump_include_dot_paths(sample_order: Order):
    result = prune_dump(
        sample_order,
        include=["id", "customer.name", "items.*.sku", "items.*.price"],
    )

    assert set(result.keys()) == {"id", "customer", "items"}
    assert result["customer"] == {"name": "Alice Corp"}
    assert result["items"] == [
        {"sku": "SKU-A", "price": 50.0},
        {"sku": "SKU-B", "price": 25.25},
    ]


def test_prune_dump_exclude_glob(sample_order: Order):
    result = prune_dump(
        sample_order,
        exclude=["*.secret_token", "audit", "items.*.notes"],
    )

    assert "audit" not in result
    assert "secret_token" not in result["customer"]
    assert "notes" not in result["items"][0]
    assert "notes" not in result["items"][1]
    assert result["items"][0]["sku"] == "SKU-A"


def test_prune_dump_exclude_namespaces_and_prefixes(sample_order: Order):
    result = prune_dump(
        sample_order,
        exclude_namespaces=["http://www.w3.org/2000/09/xmldsig#"],
        exclude_prefixes=["ext"],
    )

    # Signature excluded by namespace
    assert "signature" not in result["audit"]
    assert result["audit"]["created_by"] == "system"

    # Extension excluded by prefix
    assert "ext_data" not in result["items"][1]


def test_prune_dump_key_styles(sample_order: Order):
    # XML key style
    xml_result = prune_dump(
        sample_order,
        include=["id", "customer.name"],
        key_style="xml",
    )
    assert "ID" in xml_result
    assert "Customer" in xml_result or "customer" in xml_result
    assert xml_result["customer"]["Name"] == "Alice Corp"

    # Prefixed XML key style with ns_map
    prefixed_result = prune_dump(
        sample_order,
        include=["audit.signature"],
        key_style="prefixed_xml",
        ns_map={"ds": "http://www.w3.org/2000/09/xmldsig#"},
    )
    assert "ds:Signature" in prefixed_result["audit"]


def test_prune_dump_max_depth(sample_order: Order):
    result = prune_dump(sample_order, max_depth=1)
    # Depth 1 includes order fields, but nested structures at depth 2 are None/omitted
    assert "id" in result
    assert "customer" not in result or result["customer"] is None


def test_prune_dump_exclude_defaults(sample_order: Order):
    # quantity default is 1, so quantity=1 would be omitted if default
    sample_order.items[0].quantity = 1
    result = prune_dump(sample_order, exclude_defaults=True)
    assert "quantity" not in result["items"][0]
    assert result["items"][1]["quantity"] == 2


def test_prune_dump_scalars_and_collections():
    data = [
        {"a": 1, "b": None, "c": []},
        {"a": 2, "b": "hello", "c": [1, 2]},
    ]
    res = prune_dump(data, exclude_none=True, exclude_empty=True)
    assert res == [{"a": 1}, {"a": 2, "b": "hello", "c": [1, 2]}]

    class DummyIso:
        def isoformat(self):
            return "2026-09-13T12:00:00Z"

    assert prune_dump(DummyIso()) == "2026-09-13T12:00:00Z"
    assert prune_dump(date(2026, 9, 13)) == "2026-09-13"


def test_project_model_basic():
    class Address(BaseModel):
        street: str
        city: str
        zip_code: str

    class Person(BaseModel):
        name: str
        age: int = Field(..., ge=0)
        address: Address
        bio: str = "default bio"

    LeanPerson = project_model(
        Person,
        include={"name", "age", "address.city"},
        name="LeanPerson",
    )

    schema = LeanPerson.model_json_schema()
    assert "bio" not in schema["properties"]
    assert "street" not in schema["$defs"]["ProjectedAddress"]["properties"]
    assert "city" in schema["$defs"]["ProjectedAddress"]["properties"]
    assert schema["properties"]["age"]["minimum"] == 0

    # Test instantiation and validation
    lean = LeanPerson(
        name="Bob",
        age=30,
        address={"city": "Metropolis"},
    )
    assert lean.model_dump() == {
        "name": "Bob",
        "age": 30,
        "address": {"city": "Metropolis"},
    }

    # Validation constraint preserved
    with pytest.raises(ValueError):
        LeanPerson(name="Bob", age=-5, address={"city": "Metropolis"})

    # Hydration back to full Person
    full = Person.model_validate(
        lean.model_dump() | {"address": {"street": "Main St", "city": "Metropolis", "zip_code": "10001"}}
    )
    assert full.name == "Bob"
    assert full.bio == "default bio"


def test_project_model_list_and_optional():
    class Part(BaseModel):
        part_no: str
        weight: float

    class Machine(BaseModel):
        id: str
        parts: list[Part]
        backup_part: Part | None = None
        extra: str = "unused"

    LeanMachine = project_model(
        Machine,
        include={"id", "parts.part_no", "backup_part.part_no"},
    )

    lean = LeanMachine(
        id="M-1",
        parts=[{"part_no": "P-1"}],
        backup_part={"part_no": "P-2"},
    )
    dumped = lean.model_dump()
    assert dumped == {
        "id": "M-1",
        "parts": [{"part_no": "P-1"}],
        "backup_part": {"part_no": "P-2"},
    }


def test_project_model_xml_names():
    class XmlProduct(BaseModel):
        item_id: str = field(metadata={"name": "ItemID", "type": "Element"})
        price: float = field(metadata={"name": "Price", "type": "Element"})
        unused: str = field(metadata={"name": "Unused", "type": "Element"})

    LeanProduct = project_model(XmlProduct, include={"ItemID", "price"})
    lean = LeanProduct(item_id="123", price=9.99)
    assert lean.item_id == "123"
    assert lean.price == 9.99
    assert not hasattr(lean, "unused")


def test_project_model_no_match():
    class Sample(BaseModel):
        x: int

    with pytest.raises(ValueError, match="None of the include paths"):
        project_model(Sample, include={"non_existent"})


def test_prune_dump_prefix_from_ns_map():
    class M(BaseModel):
        val: str = field(metadata={"name": "Val", "namespace": "urn:foo"})

    obj = M(val="ok")
    res = prune_dump(obj, exclude_prefixes=["f"], ns_map={"f": "urn:foo"})
    assert res == {}


def test_prune_dump_list_with_none():
    data = [None, "keep", None]
    res = prune_dump(data, exclude_none=True)
    assert res == ["keep"]


def test_project_model_union_scalar():
    class Multi(BaseModel):
        val: int | str
        desc: str

    LeanMulti = project_model(Multi, include={"val"})
    assert LeanMulti(val="abc").val == "abc"
    assert LeanMulti(val=123).val == 123


def test_lazy_imports():
    import pyxsdata.pydantic as pyd

    assert callable(pyd.project_model)
    assert callable(pyd.prune_dump)


def test_key_style_python(sample_order: Order):
    res = prune_dump(sample_order, include=["id"], key_style="python")
    assert "id" in res


def test_prune_dump_wildcard_include(sample_order: Order):
    res = prune_dump(sample_order, include=["*.name"])
    assert res == {"customer": {"name": "Alice Corp"}}
