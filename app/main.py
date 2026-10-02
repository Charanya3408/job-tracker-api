from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from app import models  # noqa: F401
from app.database import Base, engine
from app.routers import analytics, applications, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Application Tracker API", version="0.2.0")
app.include_router(auth.router)
app.include_router(applications.router)
app.include_router(analytics.router)

STATIC_DIR = Path(__file__).parent / "static"


@app.get("/", include_in_schema=False)
def dashboard():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health():
    return {"status": "ok"}
