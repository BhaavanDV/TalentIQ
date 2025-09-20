from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api import deps
from app.schemas.job import Job, JobCreate, JobUpdate
from app.services.job_service import JobService
from app.core.security import get_current_user, get_current_active_superuser
from app.schemas.user import User

router = APIRouter()

@router.post("/", response_model=Job)
def create_job(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(get_current_active_superuser),
    job_in: JobCreate
) -> Job:
    """
    Create a new job posting (superuser only)
    """
    job_service = JobService(db)
    return job_service.create(job_in)

@router.get("/", response_model=List[Job])
def list_jobs(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
    industry: Optional[str] = None,
    location: Optional[str] = None
) -> List[Job]:
    """
    List all job postings with optional filters
    """
    job_service = JobService(db)
    filters = {}
    if industry:
        filters["industry"] = industry
    if location:
        filters["location"] = location
    return job_service.get_multi(skip=skip, limit=limit, filters=filters)

@router.get("/{job_id}", response_model=Job)
def get_job(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(get_current_user),
    job_id: int
) -> Job:
    """
    Get a specific job posting
    """
    job_service = JobService(db)
    job = job_service.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.put("/{job_id}", response_model=Job)
def update_job(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(get_current_active_superuser),
    job_id: int,
    job_in: JobUpdate
) -> Job:
    """
    Update a job posting (superuser only)
    """
    job_service = JobService(db)
    job = job_service.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job_service.update(job_id, job_in)

@router.delete("/{job_id}")
def delete_job(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(get_current_active_superuser),
    job_id: int
) -> dict:
    """
    Delete a job posting (superuser only)
    """
    job_service = JobService(db)
    job = job_service.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job_service.delete(job_id)
    return {"message": "Job deleted successfully"}