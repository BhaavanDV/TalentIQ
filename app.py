import os
from pathlib import Path
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create FastAPI app instance
app = FastAPI(
    title="TalentIQ",
    description="Smart Resume Analysis and Job Matching System",
    version="1.0.0"
)

# Database settings
DATABASE_URL = "sqlite:///./talentiq.db"
ENVIRONMENT = "development"

# Create database engine and session
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Create necessary directories
UPLOAD_DIR = Path("uploads")
MODEL_DIR = Path("models")
DATA_DIR = Path("data")

UPLOAD_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8502"],  # Streamlit app origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Resume endpoints
@app.post("/api/v1/resumes/")
async def upload_resume(file: UploadFile):
    try:
        # Create uploads directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join("uploads", filename)
        
        # Save the file
        contents = await file.read()
        with open(file_path, 'wb') as f:
            f.write(contents)
        
        return {
            "filename": filename,
            "status": "success",
            "message": "Resume uploaded successfully"
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e)
            }
        )

@app.get("/api/v1/resumes/")
async def list_resumes():
    try:
        resumes = []
        upload_dir = "uploads"
        if os.path.exists(upload_dir):
            for filename in os.listdir(upload_dir):
                file_path = os.path.join(upload_dir, filename)
                if os.path.isfile(file_path):
                    stats = os.stat(file_path)
                    resumes.append({
                        "filename": filename,
                        "size": stats.st_size,
                        "uploaded_at": stats.st_mtime
                    })
        return resumes
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e)
            }
        )

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
        "environment": "development",
        "api_version": "1.0.0"
    }

@app.get("/api/v1/jobs/")
async def list_jobs():
    # Placeholder for job listings
    return [
        {
            "id": 1,
            "title": "Software Engineer",
            "description": "Python developer position",
            "status": "active"
        }
    ]

@app.get("/api/v1/evaluations/")
async def list_evaluations():
    # Placeholder for evaluations
    return [
        {
            "id": 1,
            "resume_id": 1,
            "job_id": 1,
            "match_score": 0.85
        }
    ]

@app.post("/api/v1/analyze/skills")
async def analyze_skills(data: dict):
    try:
        # Mock skills analysis - replace with actual ML model in production
        return {
            "skills": ["Python", "Java", "AWS", "Docker", "SQL"],
            "confidence_scores": [0.95, 0.85, 0.78, 0.92, 0.88]
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e)
            }
        )

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )