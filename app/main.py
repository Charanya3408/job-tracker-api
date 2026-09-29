from fastapi import FastAPI

from app import models  # noqa: F401
from app.database import Base, engine
from app.routers import analytics, applications, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Application Tracker API", version="0.1.0")
app.include_router(auth.router)
app.include_router(applications.router)
app.include_router(analytics.router)


@app.get("/health")
def health():
    return {"status": "ok"}
