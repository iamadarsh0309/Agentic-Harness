# Parser conventions

Two rules for `sloperator/parser/parser.py`. Both are already followed by the
existing code — keep it that way.

## One method per grammar rule

Each production in the grammar block of `docs/spec.md` gets exactly one method,
named after the rule (`logic_or`, `logic_and`, `equality`, `comparison`, `term`,
`factor`, `unary`, `call`, `primary`, `block`, `var_decl`, `if_stmt`, ...).

- Don't inline a rule into its caller or split one rule across several methods.
- When the grammar changes, add or rename the method to match the spec, and update
  `docs/spec.md` in the same change.
- Helper methods that are not grammar rules (`expect`, `match`, `check`, `advance`,
  `peek`, `previous`, `at_end`, `error`, `terminator`) stay at the bottom of the class.

## Syntax errors must say what was found

Every `SlopSyntaxError` names the offending token. Route messages through
`self.error(token, message)` or `self.expect(type, message)` — never raise
`SlopSyntaxError` directly with a bare message.

`error()` appends the detail automatically:

- normal token: `"<message>, found '<lexeme>'"`
- end of input: `"<message>, but reached end of file"`

So write the message as the expectation only, e.g.
`"expected '=' after variable name, an initializer is required"` — not
`"expected '=' after variable name, found '✨'"`.

Tests in `tests/test_errors.py` assert the full stderr string, so a message change
means updating that table too.
