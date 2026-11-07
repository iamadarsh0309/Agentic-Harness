"""Regression tests for compound assignment with ``+=``.

``name += expression`` evaluates the right-hand expression first, then adds it
to the variable's current value. Numbers add, strings concatenate, and the
nearest binding is updated.
"""

import pytest

from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    assert result.exit_code == 0
    return result.stdout


def fails(source: str) -> str:
    result = run_source(source)
    assert result.exit_code == 1
    return result.stderr.rstrip("\n")


def test_plus_equal_adds_to_current_value():
    source = """slop n = 2✨
n += 3 * 4✨
hallucinate(n)✨"""
    assert run(source) == "14\n"


def test_right_hand_side_is_evaluated_before_adding():
    # 3 * 4 must be computed first, so n becomes 2 + 12 rather than (2 + 3) * 4.
    source = """slop n = 2✨
n += 3 * 4✨
hallucinate(n)✨"""
    assert run(source) == "14\n"


def test_plus_equal_accumulates_across_statements():
    source = """slop n = 0✨
n += 1✨
n += 2✨
n += 3✨
hallucinate(n)✨"""
    assert run(source) == "6\n"


def test_plus_equal_joins_strings():
    source = """slop s = “hooks”✨
s += “ work”✨
hallucinate(s)✨"""
    assert run(source) == "hooks work\n"


def test_plus_equal_updates_nearest_binding():
    source = """slop n = 1✨
{
    slop n = 2✨
    n += 10✨
    hallucinate(n)✨
}
hallucinate(n)✨"""
    assert run(source) == "12\n1\n"


def test_plus_equal_works_inside_a_function():
    source = """clanker bump(start) {
    slop total = start✨
    total += 5✨
    ship total✨
}
hallucinate(bump(1))✨"""
    assert run(source) == "6\n"


def test_plus_equal_accepts_negative_and_division_operands():
    source = """slop n = 10✨
n += -7 / 2✨
hallucinate(n)✨"""
    assert run(source) == "7\n"


def test_plus_equal_on_undefined_name_is_a_runtime_error():
    assert fails("n += 1✨") == "SlopLang runtime error at line 1: undefined variable 'n'"


def test_plus_equal_on_loadbearing_is_a_runtime_error():
    source = """loadbearing LIMIT = 1✨
LIMIT += 1✨"""
    assert fails(source) == "SlopLang runtime error at line 2: cannot assign to loadbearing 'LIMIT'"


@pytest.mark.parametrize(
    ("left", "right"),
    [
        ("1", "“x”"),
        ("“x”", "1"),
        ("✅", "1"),
    ],
)
def test_plus_equal_with_incompatible_types_is_a_runtime_error(left: str, right: str):
    source = f"""slop v = {left}✨
v += {right}✨"""
    result = run_source(source)
    assert result.exit_code == 1
    assert result.stderr.startswith("SlopLang runtime error at line 2: operands of '+=' must")
