"""Tests pour taskia/utils/formatter.py"""

from modules.taskia.utils.formatter import format_summary


def test_format_summary_simple() -> None:
    """Test du formatage avec un contexte simple"""
    context = {
        "key1": "value1",
        "key2": "value2"
    }
    expected = "- key1: value1\n- key2: value2"
    assert format_summary(context) == expected

def test_format_summary_nested() -> None:
    """Test du formatage avec un contexte imbriqué"""
    context = {
        "module": "test_module",
        "details": {
            "param1": "value1",
            "param2": 42
        }
    }
    expected = "- module: test_module\n- details: {'param1': 'value1', 'param2': 42}"
    assert format_summary(context) == expected

def test_format_summary_empty() -> None:
    """Test du formatage avec un contexte vide"""
    assert format_summary({}) == ""

def test_format_summary_special_values() -> None:
    """Test du formatage avec des valeurs spéciales"""
    context = {
        "none": None,
        "bool": True,
        "number": 42,
        "list": [1, 2, 3],
        "dict": {"a": 1, "b": 2}
    }
    expected = (
        "- none: None\n"
        "- bool: True\n"
        "- number: 42\n"
        "- list: [1, 2, 3]\n"
        "- dict: {'a': 1, 'b': 2}"
    )
    assert format_summary(context) == expected
