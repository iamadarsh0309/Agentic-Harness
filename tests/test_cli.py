import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INTERPRETER = ROOT / "sloperator.py"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(INTERPRETER), *args], capture_output=True, encoding="utf-8"
    )


def test_runs_a_file():
    completed = run_cli(str(ROOT / "examples/hello.slop"))
    assert completed.returncode == 0
    assert completed.stdout == "hello, slop\n"
    assert completed.stderr == ""


def test_error_goes_to_stderr_after_earlier_output(tmp_path: Path):
    program = tmp_path / "boom.slop"
    program.write_text("hallucinate(“before”)✨\nhallucinate(missing)✨\n", encoding="utf-8")
    completed = run_cli(str(program))
    assert completed.returncode == 1
    assert completed.stdout == "before\n"
    assert completed.stderr == "SlopLang runtime error at line 2: undefined variable 'missing'\n"
    assert "Traceback" not in completed.stderr


def test_missing_file_and_usage():
    assert run_cli().returncode == 2
    missing = run_cli(str(ROOT / "nope.slop"))
    assert missing.returncode == 2
    assert "could not read" in missing.stderr


def test_check_accepts_a_valid_file_without_executing_it(tmp_path: Path):
    program = tmp_path / "valid.slop"
    program.write_text("hallucinate(“should not run”)✨\n", encoding="utf-8")
    completed = run_cli("--check", str(program))
    assert completed.returncode == 0
    assert completed.stderr == ""
    assert "should not run" not in completed.stdout
    assert f"syntax ok: {program}\n" == completed.stdout


def test_check_reports_lexical_and_syntax_errors(tmp_path: Path):
    program = tmp_path / "bad.slop"
    program.write_text("hallucinate(“never runs”)✨\nslop x✨\n", encoding="utf-8")
    completed = run_cli("--check", str(program))
    assert completed.returncode == 1
    assert completed.stdout == ""
    assert completed.stderr == (
        "SlopLang syntax error at line 2: expected '=' after variable name,"
        " an initializer is required, found '✨'\n"
    )
    assert "Traceback" not in completed.stderr

    lexical = tmp_path / "lexical.slop"
    lexical.write_text('hallucinate("straight quotes")✨\n', encoding="utf-8")
    completed = run_cli("--check", str(lexical))
    assert completed.returncode == 1
    assert "SlopLang lexical error" in completed.stderr


def test_check_does_not_report_runtime_errors(tmp_path: Path):
    program = tmp_path / "runtime.slop"
    program.write_text("hallucinate(missing)✨\n", encoding="utf-8")
    completed = run_cli("--check", str(program))
    assert completed.returncode == 0
    assert completed.stderr == ""
    assert "missing" not in completed.stdout


def test_check_requires_exactly_one_file_and_works_in_either_position():
    usage = run_cli("--check")
    assert usage.returncode == 2
    assert "--check" in usage.stderr
    assert run_cli("--check", "a.slop", "b.slop").returncode == 2

    completed = run_cli(str(ROOT / "examples/hello.slop"), "--check")
    assert completed.returncode == 0
    assert "hello, slop" not in completed.stdout
