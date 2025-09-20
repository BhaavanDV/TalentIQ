from typing import List, Optional, Dict, Any
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.evaluation import EvaluationCreate, EvaluationUpdate, Evaluation
from app.repositories.evaluation_repository import EvaluationRepository
from app.services.resume_service import ResumeService
from app.services.job_service import JobService

class EvaluationService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = EvaluationRepository()
        self.resume_service = ResumeService(db)
        self.job_service = JobService(db)

    async def create_evaluation(
        self,
        evaluation_in: EvaluationCreate
    ) -> Evaluation:
        """
        Create a new evaluation for a resume against a job posting
        """
        # Verify resume and job exist
        resume = self.resume_service.get(evaluation_in.resume_id)
        if not resume:
            raise HTTPException(
                status_code=404,
                detail="Resume not found"
            )
            
        job = self.job_service.get(evaluation_in.job_id)
        if not job:
            raise HTTPException(
                status_code=404,
                detail="Job not found"
            )
            
        # Calculate match scores and skills analysis
        match_score = self._calculate_match_score(
            job.required_skills,
            resume.skills
        )
        
        matching_skills = self._get_matching_skills(
            job.required_skills,
            resume.skills
        )
        
        missing_skills = self._get_missing_skills(
            job.required_skills,
            resume.skills
        )
        
        # Create evaluation with calculated metrics
        evaluation_data = EvaluationCreate(
            resume_id=evaluation_in.resume_id,
            job_id=evaluation_in.job_id,
            match_score=match_score,
            matching_skills=matching_skills,
            missing_skills=missing_skills,
            status="completed"
        )
        
        return self.repository.create(self.db, obj_in=evaluation_data)

    def get(self, evaluation_id: int) -> Optional[Evaluation]:
        """
        Get an evaluation by ID
        """
        return self.repository.get(self.db, evaluation_id)

    def get_multi(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Evaluation]:
        """
        Get multiple evaluations with optional filtering
        """
        return self.repository.get_multi(
            self.db,
            skip=skip,
            limit=limit,
            filters=filters
        )

    def get_job_evaluations(
        self,
        job_id: int,
        min_score: Optional[float] = None
    ) -> List[Evaluation]:
        """
        Get all evaluations for a specific job
        Optionally filter by minimum match score
        """
        filters = {"job_id": job_id}
        evaluations = self.repository.get_multi(self.db, filters=filters)
        
        if min_score is not None:
            evaluations = [
                e for e in evaluations
                if e.match_score >= min_score
            ]
            
        return sorted(
            evaluations,
            key=lambda x: x.match_score,
            reverse=True
        )

    def get_resume_evaluations(
        self,
        resume_id: int
    ) -> List[Evaluation]:
        """
        Get all evaluations for a specific resume
        """
        filters = {"resume_id": resume_id}
        return self.repository.get_multi(self.db, filters=filters)

    def update(
        self,
        evaluation_id: int,
        evaluation_in: EvaluationUpdate
    ) -> Evaluation:
        """
        Update an evaluation
        """
        evaluation = self.repository.get(self.db, evaluation_id)
        if not evaluation:
            raise HTTPException(
                status_code=404,
                detail="Evaluation not found"
            )
        return self.repository.update(
            self.db,
            id=evaluation_id,
            obj_in=evaluation_in
        )

    def delete(self, evaluation_id: int) -> None:
        """
        Delete an evaluation
        """
        evaluation = self.repository.get(self.db, evaluation_id)
        if not evaluation:
            raise HTTPException(
                status_code=404,
                detail="Evaluation not found"
            )
        self.repository.delete(self.db, id=evaluation_id)

    def _calculate_match_score(
        self,
        required_skills: Dict[str, List[str]],
        candidate_skills: Dict[str, List[str]]
    ) -> float:
        """
        Calculate how well a candidate's skills match the job requirements
        Returns a score between 0 and 1
        """
        if not required_skills:
            return 0.0
            
        total_required = sum(len(skills) for skills in required_skills.values())
        if total_required == 0:
            return 0.0
            
        matches = 0
        for category, skills in required_skills.items():
            candidate_category_skills = set(candidate_skills.get(category, []))
            matches += len([s for s in skills if s in candidate_category_skills])
            
        return matches / total_required

    def _get_matching_skills(
        self,
        required_skills: Dict[str, List[str]],
        candidate_skills: Dict[str, List[str]]
    ) -> Dict[str, List[str]]:
        """
        Get the skills that match between requirements and candidate
        """
        matching = {}
        for category, skills in required_skills.items():
            candidate_category_skills = set(candidate_skills.get(category, []))
            matches = [s for s in skills if s in candidate_category_skills]
            if matches:
                matching[category] = matches
        return matching

    def _get_missing_skills(
        self,
        required_skills: Dict[str, List[str]],
        candidate_skills: Dict[str, List[str]]
    ) -> Dict[str, List[str]]:
        """
        Get the required skills that the candidate is missing
        """
        missing = {}
        for category, skills in required_skills.items():
            candidate_category_skills = set(candidate_skills.get(category, []))
            missing_skills = [s for s in skills if s not in candidate_category_skills]
            if missing_skills:
                missing[category] = missing_skills
        return missing