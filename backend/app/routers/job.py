from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.services.job_service import JobService
from app.schemas.job import JobCreate, JobUpdate, Job
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=Job)
async def create_job(
    job_in: JobCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new job posting
    """
    job_service = JobService(db)
    return await job_service.create_job(job_in)

@router.get("/{job_id}", response_model=Job)
def get_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific job by ID
    """
    job_service = JobService(db)
    job = job_service.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/", response_model=List[Job])
def list_jobs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all jobs
    """
    job_service = JobService(db)
    return job_service.get_multi(skip=skip, limit=limit)

@router.put("/{job_id}", response_model=Job)
def update_job(
    job_id: int,
    job_in: JobUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a job posting
    """
    job_service = JobService(db)
    return job_service.update(job_id, job_in)

@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a job posting
    """
    job_service = JobService(db)
    job_service.delete(job_id)
    return {"message": "Job deleted successfully"}