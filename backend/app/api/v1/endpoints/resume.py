from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api import deps
from app.schemas.resume import Resume, ResumeCreate, ResumeUpdate
from app.services.resume_service import ResumeService
from app.core.security import get_current_user
from app.schemas.user import User

router = APIRouter()

@router.post("/", response_model=Resume)
async def create_resume(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(get_current_user),
    file: UploadFile = File(...),
) -> Resume:
    """
    Upload and process a new resume
    """
    resume_service = ResumeService(db)
    return await resume_service.create_resume(current_user.id, file)

@router.get("/", response_model=List[Resume])
def list_resumes(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
) -> List[Resume]:
    """
    Retrieve all resumes for the current user
    """
    resume_service = ResumeService(db)
    return resume_service.get_user_resumes(current_user.id, skip, limit)

@router.get("/{resume_id}", response_model=Resume)
def get_resume(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(get_current_user),
    resume_id: int,
) -> Resume:
    """
    Get a specific resume by ID
    """
    resume_service = ResumeService(db)
    resume = resume_service.get(resume_id)
    if not resume or resume.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume

@router.delete("/{resume_id}")
def delete_resume(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(get_current_user),
    resume_id: int,
) -> dict:
    """
    Delete a resume
    """
    resume_service = ResumeService(db)
    resume = resume_service.get(resume_id)
    if not resume or resume.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    resume_service.delete(resume_id)
    return {"message": "Resume deleted successfully"}