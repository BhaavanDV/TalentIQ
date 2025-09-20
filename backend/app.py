import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create FastAPI app instance
app = FastAPI(
    title="TalentIQ",
    description="Smart Resume Analysis and Job Matching System",
    version="1.0.0"
)

# Basic settings
DATABASE_URL = "sqlite:///./talentiq.db"
ENVIRONMENT = "development"

# Create database engine and session
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Create database tables
Base.metadata.create_all(bind=engine)

# Create required directories
os.makedirs("uploads", exist_ok=True)
os.makedirs("models", exist_ok=True)
os.makedirs("data", exist_ok=True)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(resume.router, prefix="/api/v1/resumes", tags=["Resumes"])
app.include_router(job.router, prefix="/api/v1/jobs", tags=["Jobs"])
app.include_router(evaluation.router, prefix="/api/v1/evaluations", tags=["Evaluations"])

@app.get("/")
async def root():
    """
    Root endpoint - Basic health check
    """
    return {
        "message": "Welcome to TalentIQ API",
        "status": "online",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "environment": ENVIRONMENT,
        "api_version": "1.0.0"
    }

# Only import routers after database is set up
from app.routers import resume, job, evaluation

# Include routers
app.include_router(resume.router, prefix="/api/v1/resumes", tags=["Resumes"])
app.include_router(job.router, prefix="/api/v1/jobs", tags=["Jobs"])
app.include_router(evaluation.router, prefix="/api/v1/evaluations", tags=["Evaluations"])

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Enable auto-reload for development
    )
    
    