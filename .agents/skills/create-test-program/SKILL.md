---
name: create-test-program
description: >
  Given a SlopLang language feature, read docs/spec.md, write an example
  program in examples/, and add an exact-output test for it in
  tests/test_example_outputs.py
---

# Create Test Program

Given a SlopLang language feature:

1. Read `docs/spec.md` and confirm the feature's exact syntax, semantics, and
   expected behavior before writing any code.
2. Write a minimal example that exercises the feature in
   `examples/<feature>.slop`, following the style of neighboring examples
   (leading `—` comment line, statements are `hallucinate(...)✨`).
3. Run it with `uv run sloperator.py examples/<feature>.slop` and capture the
   exact output — never hand-guess it.
4. Add a test to `tests/test_example_outputs.py` (create the file if missing):
   read the example file, run it through `run_source`, and assert the exact
   `stdout` (every line), empty `stderr`, and `exit_code == 0`.
5. Format and validate per AGENTS.md: `uv run ruff format`, then
   `uv run pytest`, `uv run ruff format --check`, `uv run ruff check`,
   `uv run ty check`.
