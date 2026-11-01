---
description: Start the Sloperator playground server on $ARGUMENTS (default 8080), reusing a server that is already running
---

Here is the current list of TCP listeners:

!`lsof -nP -iTCP -sTCP:LISTEN`

The requested port is: $ARGUMENTS. If that is blank, use 8080.

Before starting anything:

1. Check the listener list above. If the requested port is already held by a
   Sloperator playground server (a python process running
   `playground/server.py`), do NOT start another one — report that the server
   is already running and reuse it.
2. Otherwise, start `uv run playground/server.py <port>` in the background,
   where `<port>` is the requested port (or 8080 if no argument was given).
3. Verify the server is listening on the requested port and report its URL.
