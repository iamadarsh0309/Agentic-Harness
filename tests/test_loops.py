from sloperator.runner import run_source


def test_ralph_false_condition_does_not_run():
    result = run_source("ralph ❌ {\nhallucinate(“never”)✨\n}\n")
    assert result.stdout == ""
    assert result.stderr == ""
    assert result.exit_code == 0
