from sloperator.runner import run_source


def test_unary_minus_rejects_boolean():
    result = run_source("hallucinate(-✅)✨")
    assert result.stdout == ""
    assert result.stderr == (
        "SlopLang runtime error at line 1: operand of unary '-' must be a number, got boolean\n"
    )
    assert result.exit_code == 1


def test_unary_minus_accepts_number():
    result = run_source("hallucinate(-1)✨")
    assert result.stdout == "-1\n"
    assert result.stderr == ""
    assert result.exit_code == 0
