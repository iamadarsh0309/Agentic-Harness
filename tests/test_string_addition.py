from sloperator.runner import run_source


def test_empty_string_on_left_concatenates():
    result = run_source("hallucinate(“” + “slop”)✨")
    assert result.stdout == "slop\n"
    assert result.stderr == ""
    assert result.exit_code == 0


def test_empty_string_on_right_concatenates():
    result = run_source("hallucinate(“slop” + “”)✨")
    assert result.stdout == "slop\n"
    assert result.stderr == ""
    assert result.exit_code == 0


def test_string_with_emoji_concatenates():
    result = run_source("hallucinate(“café” + “✨”)✨")
    assert result.stdout == "café✨\n"
    assert result.stderr == ""
    assert result.exit_code == 0
