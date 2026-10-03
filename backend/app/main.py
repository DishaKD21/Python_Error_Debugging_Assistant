from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.debug import router as debug_router

app = FastAPI(title="Python Debugging Assistant", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(debug_router)


@app.get("/")
async def root():
    return {"message": "Python Debugging Assistant API is running."}
