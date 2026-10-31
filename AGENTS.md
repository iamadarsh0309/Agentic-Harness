# AGENTS.md

Sloperator is a tree-walking interpreter for SlopLang, a joke language with emoji
syntax, written in Python 3.13.

## Layout

- `sloperator.py` — CLI entrypoint (`--check` parses without executing).
- `sloperator/runner.py` — wires the pipeline: `tokenize -> parse -> Interpreter`.
- `sloperator/lexer/` — scanner and token types.
- `sloperator/parser/` — recursive-descent parser and AST dataclasses.
- `sloperator/evaluator/` — interpreter, environments, and value helpers.
- `sloperator/errors.py` — `SlopError` subclasses; `str(error)` is the user-facing message.
- `tests/` — pytest suite. `examples/` — sample `.slop` programs.
- `playground/` — small web server and editor page.

## Validation

Run all four from the project root before finishing a change:

```bash
uv run pytest
uv run ruff format --check
uv run ruff check
uv run ty check
```

Comparison tests live in `tests/test_comparisons.py`; run them with
`uv run pytest tests/test_comparisons.py -q`.

## Regression tests

Add a regression test whenever you fix a bug or change observable behavior — a
wrong error message, a precedence fix, a crash, or a CLI exit code. Put it next to
the closest existing test file rather than creating a new one, and assert on
`run_source(source)` output (`stdout`, `stderr`, `exit_code`) or the CLI result.
Error messages are asserted exactly, so update `tests/test_errors.py` when a
message changes.

## Language behavior

`docs/spec.md` is the source of truth for syntax, semantics, operators, and error
text. Read it before changing language behavior, and update it in the same change.
