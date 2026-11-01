---
name: commit
description: Commit and push finished, validated work from the project root. Only run this when the user explicitly invokes it — never commit or push on your own.
---

# Commit

After tests and checks are complete and passing, and only when the user explicitly
invokes this skill:

1. From the project root, run `git status --short` and review the changes.
2. Stage only the files relevant to the completed work (never unrelated or
   pre-existing modifications).
3. Write a short, conventional commit message (e.g. `feat: ...`, `fix: ...`,
   `test: ...`).
4. Push to the remote: `git push origin main`.
5. Report the commit hash and push result.
