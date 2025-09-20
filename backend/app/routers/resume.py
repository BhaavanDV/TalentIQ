from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List
from sqlalchemy.orm import Session
from app.services.resume_service import ResumeService
from app.schemas.resume import ResumeCreate, ResumeUpdate, Resume
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=Resume)
async def create_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload and create a new resume
    """
    resume_service = ResumeService(db)
    return await resume_service.create_resume(user_id=1, file=file)  # TODO: Get user_id from auth

@router.get("/{resume_id}", response_model=Resume)
def get_resume(
    resume_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific resume by ID
    """
    resume_service = ResumeService(db)
    resume = resume_service.get(resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume

@router.get("/", response_model=List[Resume])
def list_resumes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all resumes
    """
    resume_service = ResumeService(db)
    return resume_service.get_user_resumes(user_id=1, skip=skip, limit=limit)  # TODO: Get user_id from auth

@router.delete("/{resume_id}")
def delete_resume(
    resume_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a resume
    """
    resume_service = ResumeService(db)
    resume_service.delete(resume_id)
    return {"message": "Resume deleted successfully"}