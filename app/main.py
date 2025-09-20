from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pathlib import Path
from datetime import datetime

# Create FastAPI app instance
app = FastAPI(
    title="TalentIQ",
    description="Smart Resume Analysis and Job Matching System",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit app origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
UPLOAD_DIR = Path("uploads")
MODEL_DIR = Path("models")
DATA_DIR = Path("data")

UPLOAD_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

@app.get("/")
async def root():
    """Root endpoint - Basic health check"""
    return {
        "message": "Welcome to TalentIQ API",
        "status": "online",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": "development",
        "timestamp": datetime.now().isoformat()
    }

# Resume endpoints
@app.get("/api/v1/resumes/")
async def list_resumes():
    """List all uploaded resumes"""
    resumes = []
    if UPLOAD_DIR.exists():
        for file_path in UPLOAD_DIR.glob("*"):
            if file_path.is_file():
                stats = file_path.stat()
                resumes.append({
                    "filename": file_path.name,
                    "size": stats.st_size,
                    "uploaded_at": datetime.fromtimestamp(stats.st_mtime).isoformat()
                })
    return resumes

@app.get("/api/v1/jobs/")
async def list_jobs():
    """List available jobs"""
    return [
        {
            "id": 1,
            "title": "Software Engineer",
            "description": "Python developer position",
            "status": "active"
        }
    ]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)