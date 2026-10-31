# AGENTS.md

Sloperator: a tree-walking interpreter for SlopLang (a joke language with emoji
syntax), written in Python 3.13. `docs/spec.md` is the language source of truth;
`README.md` is the short version.

## Commands

Run from the project root. Everything goes through `uv`; there is no venv activation step.

```bash
uv run pytest tests/test_errors.py -q          # one file
uv run pytest tests/test_errors.py -k unary    # one test
uv run sloperator.py examples/fib.slop         # run a program
uv run sloperator.py --check examples/fib.slop # lex+parse only, no execution
uv run playground/server.py                    # playground on :8080
```

Full validation (also available as the `validate` skill): `uv run pytest`,
`uv run ruff format --check`, `uv run ruff check`, `uv run ty check`.
Ruff config lives in `pyproject.toml` (line length 100, rules `E,F,I,UP,B`).

## Architecture

Pipeline is strictly `tokenize -> parse -> Interpreter`, wired in `sloperator/runner.py`:

- `sloperator/lexer/scanner.py` — hand-written scanner. Emoji tokens, smart quotes,
  em-dash comments, and friendly errors for common mistakes (`"`, `;`, `//`, en dash).
- `sloperator/parser/parser.py` — recursive descent; `ast.py` holds frozen dataclasses.
- `sloperator/evaluator/interpreter.py` — `match`-based tree walker, plus `environment.py`
  (scopes) and `values.py` (`Value` union, `type_name`, `stringify`, `values_equal`).
- `sloperator/errors.py` — `SlopError` subclasses carry `kind` (`lexical`/`syntax`/`runtime`)
  and a line number; `str(error)` is the exact user-facing message.

Adding a language feature usually touches all four layers plus `docs/spec.md`.

## Testing conventions

- Most tests call `run_source(source)` from `sloperator.runner` and assert on the
  returned `RunResult` (`stdout`, `stderr`, `exit_code`) — not on internals.
- Error tests assert the **exact** stderr string, e.g.
  `"SlopLang runtime error at line 1: division by zero\n"`. `tests/test_errors.py`
  is a parametrized table; add a row there rather than a new file for a new message.
- `tests/test_examples.py` runs every `examples/*.slop` and requires non-empty stdout,
  so a new example must print something.
- `tests/test_cli.py` shells out to `sloperator.py` via `sys.executable`.

## Gotchas

- **`bool` is an `int` in Python.** Never use bare `isinstance(x, int)` for number checks;
  use `is_number()` in `interpreter.py`, which excludes `bool`. Same for `type_name()`.
- **Division truncates toward zero**, not floor (`-7 / 2 == -3`). Don't "simplify" to `//`.
- **No Python tracebacks may reach the user.** Errors are caught as `SlopError` and printed
  as `SlopLang <kind> error at line N: <message>`. Recursion is capped at
  `MAX_CALL_DEPTH = 500` and reported as `stack overflow`.
- **`ship` is implemented as a `ShipSignal` exception**, not a return value.
- **`clanker` declarations are top-level only**; the parser tracks `function_depth` to
  reject `ship` outside a function.
- **`✨` never follows a closing brace**; it terminates declarations, assignments, `ship`,
  and expression statements.
- **Emoji may carry a trailing U+FE0F variation selector** — the scanner consumes it.
- **`hallucinate` is variadic** and is the only built-in.
- **`logs/` is gitignored and watcher-ignored** (playground writes `logs/runs.log`).
  Don't commit it or treat it as source.
- **`.env` is off-limits** — `opencode.jsonc` denies reading it. Use `.env.example` for
  the shape of expected variables.
- **`uv.lock` is in `.ignore`**, so it is hidden from search tools; it is still tracked.

## Repo-specific tooling

- `.opencode/plugins/run-slop.ts` registers a `run_slop` tool that runs
  `uv run --no-active sloperator.py <path>`; prefer it over shelling out.
- `opencode.jsonc` allows `bootdev run *` without prompting; other shell commands ask.
- Lessons are submitted with `bootdev run -s <session-id>` from the project root.
