from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.services.evaluation_service import EvaluationService
from app.schemas.evaluation import EvaluationCreate, EvaluationUpdate, Evaluation
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=Evaluation)
async def create_evaluation(
    evaluation_in: EvaluationCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new evaluation
    """
    evaluation_service = EvaluationService(db)
    return await evaluation_service.create_evaluation(evaluation_in)

@router.get("/{evaluation_id}", response_model=Evaluation)
def get_evaluation(
    evaluation_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific evaluation by ID
    """
    evaluation_service = EvaluationService(db)
    evaluation = evaluation_service.get(evaluation_id)
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return evaluation

@router.get("/job/{job_id}", response_model=List[Evaluation])
def get_job_evaluations(
    job_id: int,
    min_score: float = None,
    db: Session = Depends(get_db)
):
    """
    Get all evaluations for a specific job
    """
    evaluation_service = EvaluationService(db)
    return evaluation_service.get_job_evaluations(job_id, min_score)

@router.get("/resume/{resume_id}", response_model=List[Evaluation])
def get_resume_evaluations(
    resume_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all evaluations for a specific resume
    """
    evaluation_service = EvaluationService(db)
    return evaluation_service.get_resume_evaluations(resume_id)

@router.delete("/{evaluation_id}")
def delete_evaluation(
    evaluation_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an evaluation
    """
    evaluation_service = EvaluationService(db)
    evaluation_service.delete(evaluation_id)
    return {"message": "Evaluation deleted successfully"}