"""Regression tests for the lexer's catch-all ``unexpected character`` path.

The scanner raises ``LexicalError`` from a fall-through branch for any
character that appears in no token table (``scanner.py``). It was previously
exercised only with ``#`` at the unit level and never through ``run_source``,
so this pins both: every unmapped character must raise, and the error must
surface end-to-end with the right line, message, and exit code.
"""

import pytest

from sloperator.errors import LexicalError
from sloperator.lexer import tokenize
from sloperator.runner import run_source


@pytest.mark.parametrize("ch", ["@", "$", "%", "^", "~"])
def test_unmapped_character_raises_catch_all_lexical_error(ch: str):
    with pytest.raises(LexicalError) as info:
        tokenize(f"a {ch} b")
    assert info.value.line == 1
    assert info.value.message == f"unexpected character '{ch}'"
    assert str(info.value) == f"SlopLang lexical error at line 1: unexpected character '{ch}'"


def test_catch_all_lexical_error_end_to_end():
    # Lexing fails before execution, so even the valid line 1 produces no output.
    result = run_source("hallucinate(“ok”)✨\nslop x = 1 @ 2✨")
    assert result.stdout == ""
    assert result.stderr == "SlopLang lexical error at line 2: unexpected character '@'\n"
    assert result.exit_code == 1
