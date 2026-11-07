"""Parser-level tests for the compound assignment operator ``+=``.

These cover recognition and parsing only: ``+=`` must produce an ``Assign``
statement whose operator token is ``PLUS_EQUAL`` and whose value is the full
right-hand expression.
"""

import pytest

from sloperator.errors import SlopSyntaxError
from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Assign, Binary, Literal, Variable


def parse_source(source: str):
    return parse(tokenize(source))


def only_statement(source: str):
    (statement,) = parse_source(source)
    return statement


def test_plus_equal_lexes_as_one_token():
    tokens = tokenize("n += 1✨")
    assert [token.type for token in tokens] == [
        TokenType.IDENTIFIER,
        TokenType.PLUS_EQUAL,
        TokenType.NUMBER,
        TokenType.SPARKLES,
        TokenType.EOF,
    ]
    assert tokens[1].lexeme == "+="


def test_plus_still_lexes_as_plus():
    tokens = tokenize("n + 1✨")
    assert tokens[1].type is TokenType.PLUS
    assert tokens[1].lexeme == "+"


def test_plus_equal_parses_as_assign_statement():
    statement = only_statement("n += 1✨")
    assert isinstance(statement, Assign)
    assert statement.name.lexeme == "n"
    assert statement.operator.type is TokenType.PLUS_EQUAL
    assert isinstance(statement.value, Literal)
    assert statement.value.value == 1


def test_plus_equal_keeps_full_right_hand_expression():
    statement = only_statement("n += 3 * 4✨")
    assert isinstance(statement, Assign)
    assert statement.operator.type is TokenType.PLUS_EQUAL
    assert isinstance(statement.value, Binary)
    assert statement.value.operator.type is TokenType.STAR


def test_plus_equal_accepts_arbitrary_expression():
    statement = only_statement("n += a + b✨")
    assert isinstance(statement, Assign)
    assert isinstance(statement.value, Binary)
    assert isinstance(statement.value.left, Variable)
    assert statement.value.left.name.lexeme == "a"


def test_plain_assignment_still_parses():
    statement = only_statement("n = 1✨")
    assert isinstance(statement, Assign)
    assert statement.operator.type is TokenType.EQUAL


def test_plus_equal_requires_terminator():
    with pytest.raises(SlopSyntaxError) as info:
        parse_source("n += 1")
    assert info.value.message == "expected ✨ after assignment, but reached end of file"


def test_plus_equal_requires_an_expression():
    with pytest.raises(SlopSyntaxError):
        parse_source("n += ✨")
