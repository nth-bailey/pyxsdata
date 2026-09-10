import pytest

from pyxsdata.formats.dataclass.typing import (
    evaluate,
    evaluate_attribute,
    evaluate_attributes,
    evaluate_element,
    evaluate_elements,
    evaluate_wildcard,
)
from tests.formats.dataclass.cases import (
    attribute,
    attributes,
    element,
    elements,
    wildcard,
)


def test_evaluate_with_typevar() -> None:
    result = evaluate(type["str"], None)
    assert result is str

    with pytest.raises(TypeError):
        evaluate(type["str", "int"], None)


@pytest.mark.parametrize("case,expected", attribute.tokens)
def test_evaluate_attribute_with_tokens(case, expected) -> None:
    if expected:
        assert expected == evaluate_attribute(case, tokens=True)
    else:
        with pytest.raises(TypeError):
            evaluate_attribute(case, tokens=True)


@pytest.mark.parametrize("case,expected", attribute.not_tokens)
def test_evaluate_attribute_without_tokens(case, expected) -> None:
    if expected:
        assert expected == evaluate_attribute(case, tokens=False)
    else:
        with pytest.raises(TypeError):
            evaluate_attribute(case, tokens=False)


@pytest.mark.parametrize("case,expected", attributes.cases)
def test_evaluate_attributes(case, expected) -> None:
    if expected:
        assert expected == evaluate_attributes(case)
    else:
        with pytest.raises(TypeError):
            evaluate_attributes(case)


@pytest.mark.parametrize("case,expected", element.tokens)
def test_evaluate_element_with_tokens(case, expected) -> None:
    if expected:
        assert expected == evaluate_element(case, tokens=True)
    else:
        with pytest.raises(TypeError):
            evaluate_element(case, tokens=True)


@pytest.mark.parametrize("case,expected", element.not_tokens)
def test_evaluate_element_without_tokens(case, expected) -> None:
    if expected:
        assert expected == evaluate_element(case, tokens=False)
    else:
        with pytest.raises(TypeError):
            evaluate_element(case, tokens=False)


@pytest.mark.parametrize("case,expected", elements.cases)
def test_evaluate_elements(case, expected) -> None:
    if expected:
        assert expected == evaluate_elements(case)
    else:
        with pytest.raises(TypeError):
            evaluate_elements(case)


@pytest.mark.parametrize("case,expected", wildcard.cases)
def test_evaluate_wildcard(case, expected) -> None:
    if expected:
        assert expected == evaluate_wildcard(case)
    else:
        with pytest.raises(TypeError):
            evaluate_wildcard(case)


def test_unwrap_type() -> None:
    from typing import NewType

    from pyxsdata.formats.dataclass.typing import unwrap_type

    UserId = NewType("UserId", int)
    SpecialUserId = NewType("SpecialUserId", UserId)

    assert unwrap_type(int) is int
    assert unwrap_type(UserId) is int
    assert unwrap_type(SpecialUserId) is int


def test_evaluate_with_newtype() -> None:
    from typing import NewType

    UserId = NewType("UserId", int)
    Speed = NewType("Speed", float)
    CustomStr = NewType("CustomStr", str)

    assert evaluate(UserId, None) is int
    assert evaluate(type[UserId], None) is int

    res_attr = evaluate_attribute(CustomStr, tokens=False)
    assert res_attr.types == (str,)

    res_elem = evaluate_element(Speed, tokens=False)
    assert res_elem.types == (float,)

    res_elem_opt = evaluate_element(Speed | None, tokens=False)
    assert res_elem_opt.types == (float,)
    assert res_elem_opt.optional is True

    res_elem_list = evaluate_element(list[Speed], tokens=False)
    assert res_elem_list.types == (float,)
    assert res_elem_list.factory is list

    ObjType = NewType("ObjType", object)
    res_wc = evaluate_wildcard(ObjType)
    assert res_wc.types == (object,)
