import io
import zipfile
from typing import List

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.services.gemini import debug_with_gemini

router = APIRouter(prefix="/api")


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/debug")
async def debug(files: List[UploadFile] = File(...), traceback_text: str = Form(default="")):
    if not files:
        raise HTTPException(status_code=400, detail="At least one uploaded file is required.")

    project_files: dict[str, str] = {}

    for file in files:
        if not file.filename:
            continue
        filename = file.filename
        lower_name = filename.lower()
        content = await file.read()

        if lower_name.endswith(".zip"):
            try:
                with zipfile.ZipFile(io.BytesIO(content)) as archive:
                    for info in archive.infolist():
                        if info.is_dir():
                            continue
                        inner_name = info.filename
                        if inner_name.lower().endswith(".py"):
                            project_files[inner_name] = archive.read(info.filename).decode("utf-8", errors="replace")
            except zipfile.BadZipFile:
                raise HTTPException(status_code=400, detail="The uploaded ZIP file is invalid.")
            continue

        if lower_name.endswith(".py"):
            project_files[filename] = content.decode("utf-8", errors="replace")

    if not project_files:
        raise HTTPException(status_code=400, detail="No valid Python files were uploaded.")

    response = debug_with_gemini(project_files, traceback_text or "")
    return response
