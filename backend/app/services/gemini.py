import json
import re
from typing import Any

from google import genai

from app.config import GEMINI_API_KEY, MODEL_NAME
from app.prompts.debugging_prompt import build_debugging_prompt


def _error_result(
    error_type: str,
    message: str,
    root_cause: str,
    explanation: str,
) -> dict[str, Any]:
    return {
        "status": "error",
        "error": {
            "type": error_type,
            "message": message,
            "file": None,
            "line": None,
        },
        "root_cause": root_cause,
        "explanation": explanation,
        "corrected_code": None,
        "changes": None,
        "tests": [],
    }


def _coerce_json_response(raw: str) -> dict[str, Any]:
    cleaned = raw.strip()

    # Remove markdown JSON fences if Gemini adds them
    cleaned = re.sub(
        r"^```json\s*",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    cleaned = re.sub(
        r"^```\s*",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    cleaned = re.sub(
        r"\s*```$",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    cleaned = cleaned.strip()

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        return _error_result(
            error_type="ResponseFormatError",
            message=f"Gemini returned invalid JSON: {exc}",
            root_cause="Gemini did not return the required JSON structure.",
            explanation=(
                "The model response could not be parsed as JSON. "
                "Check the Gemini prompt and response configuration."
            ),
        )

    if not isinstance(parsed, dict):
        return _error_result(
            error_type="ResponseFormatError",
            message="Gemini returned JSON, but it was not a JSON object.",
            root_cause="The Gemini response has an unexpected structure.",
            explanation="The debugging assistant requires a JSON object.",
        )

    if "status" not in parsed:
        parsed["status"] = "error"

    if "tests" not in parsed or parsed["tests"] is None:
        parsed["tests"] = []

    return parsed


def debug_with_gemini(
    project_files: dict[str, str],
    traceback_text: str,
) -> dict[str, Any]:

    # ---------------------------------------------------------
    # 1. Check API key
    # ---------------------------------------------------------

    if not GEMINI_API_KEY:
        return _error_result(
            error_type="ConfigurationError",
            message="GEMINI_API_KEY is not configured.",
            root_cause="The backend could not find GEMINI_API_KEY.",
            explanation=(
                "Make sure GEMINI_API_KEY exists in backend/.env "
                "and restart the FastAPI server."
            ),
        )

    # ---------------------------------------------------------
    # 2. Build prompt from ACTUAL uploaded files
    # ---------------------------------------------------------

    prompt = build_debugging_prompt(
        project_files,
        traceback_text,
    )

    try:

        # -----------------------------------------------------
        # 3. Create Gemini client
        # -----------------------------------------------------

        client = genai.Client(api_key=GEMINI_API_KEY)

        # -----------------------------------------------------
        # 4. Send request to Gemini
        # -----------------------------------------------------

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        # -----------------------------------------------------
        # 5. Extract response
        # -----------------------------------------------------

        text = getattr(response, "text", None)

        if not text:
            return _error_result(
                error_type="EmptyGeminiResponse",
                message="Gemini returned an empty response.",
                root_cause="The Gemini API request completed but no text was returned.",
                explanation=("Check the selected Gemini model and API response."),
            )

        # -----------------------------------------------------
        # 6. Convert Gemini JSON to Python dictionary
        # -----------------------------------------------------

        return _coerce_json_response(text)

    except Exception as exc:

        # IMPORTANT:
        # Do NOT hide the actual Gemini error.

        print("\n========== GEMINI ERROR ==========")
        print(type(exc).__name__)
        print(str(exc))
        print("==================================\n")

        return _error_result(
            error_type="GeminiAPIError",
            message=f"{type(exc).__name__}: {str(exc)}",
            root_cause="The Gemini API request failed.",
            explanation=(
                "The API key was loaded successfully, but Gemini "
                "returned an error while processing the request."
            ),
        )
