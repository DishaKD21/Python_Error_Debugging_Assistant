import json
import subprocess
import tempfile
from pathlib import Path

from app.services.gemini import debug_with_gemini


def _write_project_files(temp_dir: Path, project_files: dict[str, str]):
    for file_name, content in project_files.items():
        target = temp_dir / file_name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


def _resolve_fix_targets(project_files: dict[str, str], fixes: list[dict]) -> dict[str, str]:
    overwrite_map: dict[str, str] = {}
    for fix in fixes:
        file_name = fix.get("file")
        if not file_name:
            continue
        fixed_code = fix.get("fixed_code")
        if fixed_code:
            overwrite_map[file_name] = fixed_code
    return overwrite_map


def _write_generated_tests(temp_dir: Path, tests: list[dict]):
    if not tests:
        return

    test_code = "\n\n".join(test.get("code", "") for test in tests if test.get("code"))
    if not test_code.strip():
        return

    (temp_dir / "test_generated.py").write_text(test_code, encoding="utf-8")


def _run_pytest(temp_dir: Path):
    result = subprocess.run(
        ["pytest", "-q"],
        cwd=temp_dir,
        capture_output=True,
        text=True,
        timeout=40,
    )
    return {
        "exit_code": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "passed": result.returncode == 0,
    }


def debug_project(project_files: dict[str, str], traceback_text: str) -> dict:
    analysis = debug_with_gemini(project_files, traceback_text)

    fixes = analysis.get("fixes") or []
    tests = analysis.get("tests") or []

    with tempfile.TemporaryDirectory(prefix="debug_session_") as tmp_dir_name:
        temp_dir = Path(tmp_dir_name)
        _write_project_files(temp_dir, project_files)

        overwrite_map = _resolve_fix_targets(project_files, fixes)
        for file_name, fixed_code in overwrite_map.items():
            target = temp_dir / file_name
            target.write_text(fixed_code, encoding="utf-8")

        _write_generated_tests(temp_dir, tests)
        pytest_result = _run_pytest(temp_dir)

    analysis["verification"] = {
        "verified": pytest_result["passed"],
        "pytest_exit_code": pytest_result["exit_code"],
        "stdout": pytest_result["stdout"],
        "stderr": pytest_result["stderr"],
        "tests_passed": pytest_result["passed"],
        "tests_failed": 0 if pytest_result["passed"] else 1,
    }
    return analysis
