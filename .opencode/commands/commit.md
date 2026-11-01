---
description: Review the project diff, commit it with a message, then rebase onto origin/main
---

Review the diff of project changes before committing anything:

!`git status --short && git diff && git diff --cached`

If the changes look coherent, stage the working-tree changes, commit them with
"$ARGUMENTS" as the commit message, then run `git pull --rebase origin main`.
Report the resulting commit hash and the rebase output.
