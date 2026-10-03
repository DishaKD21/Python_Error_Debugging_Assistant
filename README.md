# Python Error Debugging Assistant

A simple FastAPI + React application for debugging uploaded Python projects by analyzing traceback information and generating a fix plus pytest verification.

## Backend

```bash
cd backend
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Frontend

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

## Notes

- Gemini is optional. If no `GEMINI_API_KEY` is set, the app falls back to a deterministic demo response for local hacking and demo work.
- Uploaded files are combined into a temp project folder and pytest is run against generated validation tests.
