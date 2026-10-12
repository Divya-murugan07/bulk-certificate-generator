from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routes import router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bulk Certificate Generator API",
    description="API for generating and managing certificates in bulk",
    version="1.0.0",
)

# Register API routes
app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "Welcome to the Bulk Certificate Generator API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "configured",
    }