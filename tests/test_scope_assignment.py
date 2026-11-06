"""Regression tests for assignment through nested brace blocks.

A bare ``{ ... }`` block used to be parented to the global scope instead of the
enclosing one, so an assignment inside a nested block skipped the nearest
binding and mutated the outer variable instead.
"""

from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    assert result.exit_code == 0
    return result.stdout


def test_assignment_in_nested_block_updates_nearest_binding():
    source = """slop score = 1✨
{
    slop score = 2✨
    {
        score = 3✨
    }
    hallucinate(score)✨
}
hallucinate(score)✨"""
    assert run(source) == "3\n1\n"


def test_assignment_in_single_block_updates_outer_binding():
    source = """slop x = 1✨
{
    x = 2✨
}
hallucinate(x)✨"""
    assert run(source) == "2\n"


def test_assignment_in_deeply_nested_blocks_updates_nearest_binding():
    source = """slop x = 0✨
{
    slop x = 1✨
    {
        slop x = 2✨
        {
            x = 3✨
        }
        hallucinate(x)✨
    }
    hallucinate(x)✨
}
hallucinate(x)✨"""
    assert run(source) == "3\n1\n0\n"


def test_block_scope_does_not_leak_declarations():
    source = """{
    slop inner = 1✨
}
hallucinate(inner)✨"""
    result = run_source(source)
    assert result.exit_code == 1
    assert result.stderr == "SlopLang runtime error at line 4: undefined variable 'inner'\n"


def test_block_can_read_enclosing_binding():
    source = """slop outer = 7✨
{
    hallucinate(outer)✨
}"""
    assert run(source) == "7\n"
