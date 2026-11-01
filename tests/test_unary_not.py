from sloperator.runner import run_source


def test_not_negates_true():
    result = run_source("hallucinate(!✅)✨")
    assert result.stdout == "❌\n"
    assert result.stderr == ""
    assert result.exit_code == 0


def test_not_negates_false():
    result = run_source("hallucinate(!❌)✨")
    assert result.stdout == "✅\n"
    assert result.stderr == ""
    assert result.exit_code == 0


def test_double_not_flips_back():
    result = run_source("hallucinate(!!✅)✨")
    assert result.stdout == "✅\n"
    assert result.stderr == ""
    assert result.exit_code == 0


def test_combined_not_operands():
    result = run_source("hallucinate(!✅, !❌, !!✅)✨")
    assert result.stdout == "❌ ✅ ✅\n"
    assert result.stderr == ""
    assert result.exit_code == 0


def test_not_rejects_number():
    result = run_source("hallucinate(!1)✨")
    assert result.stdout == ""
    assert result.stderr == (
        "SlopLang runtime error at line 1: operand of unary '!' must be a boolean, got number\n"
    )
    assert result.exit_code == 1


def test_not_rejects_string():
    result = run_source("hallucinate(!“a”)✨")
    assert result.stdout == ""
    assert result.stderr == (
        "SlopLang runtime error at line 1: operand of unary '!' must be a boolean, got string\n"
    )
    assert result.exit_code == 1
