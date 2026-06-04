from fastapi import FastAPI
from . import models
from .database import engine
from .api import projects, places

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Travel Planner API", docs_url="/docs", redoc_url="/redoc")

app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(places.router, prefix="/projects", tags=["Places"])

@app.get("/")
def root():
    return {"message": "Travel Planner API is running", "docs": "/docs"}