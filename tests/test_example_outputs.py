from pathlib import Path

from sloperator.runner import run_source

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


def test_equality_example_output():
    source = (EXAMPLES / "equality.slop").read_text(encoding="utf-8")
    result = run_source(source)
    assert result.stdout == "✅\n❌\n❌\n"
    assert result.stderr == ""
    assert result.exit_code == 0


def test_short_circuit_example_output():
    source = (EXAMPLES / "short-circuit.slop").read_text(encoding="utf-8")
    result = run_source(source)
    assert result.stdout == "❌\n✅\n"
    assert result.stderr == ""
    assert result.exit_code == 0
