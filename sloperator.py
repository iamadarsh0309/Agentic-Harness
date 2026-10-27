import sys
from pathlib import Path

from sloperator.runner import check_program, run_program


def main(argv: list[str]) -> int:
    check = "--check" in argv[1:]
    args = [arg for arg in argv[1:] if arg != "--check"]
    if len(args) != 1:
        print("usage: uv run sloperator.py [--check] <file.slop>", file=sys.stderr)
        return 2

    path = Path(args[0])
    try:
        source = path.read_text(encoding="utf-8")
    except OSError as error:
        print(f"could not read '{path}': {error.strerror}", file=sys.stderr)
        return 2

    if check:
        error = check_program(source)
        if error is not None:
            print(error, file=sys.stderr)
            return 1
        print(f"syntax ok: {path}")
        return 0

    error = run_program(source, sys.stdout)
    if error is not None:
        sys.stdout.flush()
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
