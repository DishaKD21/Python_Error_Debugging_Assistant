import re
from typing import Optional


def parse_traceback(traceback_text: str) -> dict:
    text = (traceback_text or "").strip()
    if not text:
        return {
            "error_type": "Exception",
            "message": "No traceback provided",
            "file": None,
            "line": None,
        }

    error_type = "Exception"
    message = "Unknown error"
    file_name: Optional[str] = None
    line_no: Optional[int] = None

    error_match = re.search(r"([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.+)", text, flags=re.MULTILINE | re.DOTALL)
    if error_match:
        error_type = error_match.group(1)
        message = error_match.group(2).strip()

    file_match = re.search(r'File "([^"]+)", line (\d+)', text)
    if file_match:
        file_name = file_match.group(1)
        line_no = int(file_match.group(2))

    for line in reversed(text.splitlines()):
        last_error = re.search(r"([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.+)", line.strip())
        if last_error:
            error_type = last_error.group(1)
            message = last_error.group(2).strip()
            break

    return {
        "error_type": error_type,
        "message": message,
        "file": file_name,
        "line": line_no,
    }
