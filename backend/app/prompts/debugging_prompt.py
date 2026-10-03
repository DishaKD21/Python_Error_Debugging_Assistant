def build_debugging_prompt(project_files: dict[str, str], traceback_text: str) -> str:
    file_sections = []
    for file_name, content in project_files.items():
        file_sections.append(f"--- {file_name} ---\n{content}\n")

    files_block = "\n".join(file_sections) if file_sections else "No Python files were provided by the user."
    supplied_traceback = traceback_text.strip() if traceback_text else "No traceback was provided."

    response_schema = """
{
  "status": "<success|error>",
  "error": {
    "type": "<string or null>",
    "message": "<string or null>",
    "file": "<string or null>",
    "line": "<number or null>"
  },
  "root_cause": "<string or null>",
  "explanation": "<string>",
  "corrected_code": {
    "file": "<string>",
    "code": "<string>"
  },
  "changes": "<string or null>",
  "tests": [
    {
      "name": "<string>",
      "code": "<string>"
    }
  ]
}
""".strip()

    prompt_sections = [
        "You are an expert Python debugging assistant.",
        "",
        "Analyze only the Python files uploaded by the user.",
        "Inspect the source code and relationships between the uploaded files, including imports between them.",
        "The uploaded files are the only source of truth. Their names, structure, code, and behavior are dynamic.",
        "",
        "Do not assume any filename, module, function, class, variable, library, project structure, error, or test case.",
        "Do not invent missing files or code. If an imported dependency is absent, identify it as a missing dependency.",
        "Do not use placeholder diagnoses such as an unknown error when the uploaded source can be analyzed.",
        "Do not mention files or symbols that are not present in the uploaded files or optional traceback.",
        "",
        "If the code is valid based on the available source and optional traceback, return status \"success\", error null, corrected_code null, changes null, and tests an empty list.",
        "For valid code, explain that no errors were found in the uploaded Python code based on the available evidence.",
        "If an error exists, identify the actual file and line when possible, explain the actual root cause, provide corrected code for the relevant uploaded file, explain the change, and generate tests only when they are useful for that code.",
        "",
        "Return only valid JSON matching this schema. The values in this schema are type descriptions, not values to copy:",
        response_schema,
        "",
        "Rules:",
        "- Do not return markdown fences or prose outside the JSON object.",
        "- Use status \"success\" for a no-error result and status \"error\" when a real problem is identified.",
        "- Use the optional traceback as additional evidence when it is provided.",
        "- If no traceback is provided, analyze the uploaded source code itself for syntax, runtime, logical, import, and other Python problems.",
        "- Use actual values from the uploaded files and traceback; do not copy schema descriptions into the response.",
        "",
        "USER'S ACTUAL UPLOADED FILES:",
        files_block,
        "",
        "OPTIONAL TRACEBACK OR ERROR CONTEXT:",
        supplied_traceback,
    ]

    return "\n".join(prompt_sections).strip()
