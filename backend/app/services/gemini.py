import json
import re
from typing import Any

from google import genai

from app.config import GEMINI_API_KEY, MODEL_NAME
from app.prompts.debugging_prompt import build_debugging_prompt


def _fallback_debug_result() -> dict[str, Any]:
    return {
        "status": "error",
        "error": {
            "type": "ConfigurationError",
            "message": "Gemini API key is not configured or the API request failed.",
            "file": None,
            "line": None,
        },
        "root_cause": "The backend could not contact Gemini for code analysis.",
        "explanation": "Set GEMINI_API_KEY in the backend environment and retry with the actual uploaded Python files.",
        "corrected_code": None,
        "changes": "Backend configuration is required before code analysis can run.",
        "tests": [],
    }


def _coerce_json_response(raw: str) -> dict[str, Any]:
    cleaned = raw.strip()
    cleaned = re.sub(r"```json\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"```\s*$", "", cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.strip()

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        return {
            "status": "error",
            "error": {
                "type": "ResponseFormatError",
                "message": "Gemini returned a non-JSON response.",
                "file": None,
                "line": None,
            },
            "root_cause": "The model did not return the required structured JSON.",
            "explanation": "Retry the request or check the backend Gemini response configuration.",
            "corrected_code": None,
            "changes": "The application requires structured JSON output from the model.",
            "tests": [],
        }

    if "status" not in parsed:
        parsed["status"] = "error"
    if "error" in parsed and parsed["error"] is None:
        parsed["error"] = None
    if parsed.get("tests") is None:
        parsed["tests"] = []
    return parsed


def debug_with_gemini(project_files: dict[str, str], traceback_text: str) -> dict[str, Any]:
    if not GEMINI_API_KEY:
        return _fallback_debug_result()

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        prompt = build_debugging_prompt(project_files, traceback_text)
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )
        text = getattr(response, "text", "") or ""
        if not text:
            return _fallback_debug_result()
        return _coerce_json_response(text)
    except Exception:
        return _fallback_debug_result()
