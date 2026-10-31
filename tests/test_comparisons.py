from sloperator.runner import run_source


def test_equality_binds_looser_than_comparison():
    result = run_source("hallucinate(1 < 2 == ✅)✨")
    assert result.stdout == "✅\n"
    assert result.stderr == ""
    assert result.exit_code == 0


def test_equality_binds_looser_than_comparison_with_false():
    result = run_source("hallucinate(1 < 2 == ❌)✨")
    assert result.stdout == "❌\n"
    assert result.stderr == ""
    assert result.exit_code == 0


def test_comparison_still_binds_tighter_than_and():
    result = run_source("hallucinate(1 < 2 && 2 < 3)✨")
    assert result.stdout == "✅\n"
    assert result.stderr == ""
    assert result.exit_code == 0
