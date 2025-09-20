from typing import List, Optional, Dict, Any
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.job import JobCreate, JobUpdate, Job
from app.repositories.job_repository import JobRepository
from app.services.skills_extraction_service import SkillsExtractionService

class JobService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = JobRepository()
        self.skills_extractor = SkillsExtractionService()

    async def create_job(self, job_in: JobCreate) -> Job:
        """
        Create a new job posting
        """
        # Extract skills from job description
        skills = await self.skills_extractor.extract_skills(job_in.description)
        job_in.required_skills = skills
        
        # Create job entry
        return self.repository.create(self.db, obj_in=job_in)

    def get(self, job_id: int) -> Optional[Job]:
        """
        Get a job by ID
        """
        return self.repository.get(self.db, job_id)

    def get_multi(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Job]:
        """
        Get multiple jobs with optional filtering
        """
        return self.repository.get_multi(
            self.db,
            skip=skip,
            limit=limit,
            filters=filters
        )

    def update(self, job_id: int, job_in: JobUpdate) -> Job:
        """
        Update a job posting
        """
        job = self.repository.get(self.db, job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
            
        # If description is updated, re-extract skills
        if job_in.description:
            skills =  self.skills_extractor.extract_skills(job_in.description)
            job_in.required_skills = skills
            
        return self.repository.update(self.db, id=job_id, obj_in=job_in)

    def delete(self, job_id: int) -> None:
        """
        Delete a job posting
        """
        job = self.repository.get(self.db, job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        self.repository.delete(self.db, id=job_id)

    async def search_matching_candidates(
        self,
        job_id: int,
        min_match_score: float = 0.6
    ) -> List[Dict[str, Any]]:
        """
        Search for candidates matching the job requirements
        Returns a list of candidates with their match scores
        """
        job = self.get(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
            
        # Get candidates from database
        candidates = self.repository.get_candidates_with_resumes(self.db)
        
        matches = []
        for candidate in candidates:
            match_score = self._calculate_match_score(
                job.required_skills,
                candidate.resume.skills
            )
            
            if match_score >= min_match_score:
                matches.append({
                    "candidate_id": candidate.id,
                    "match_score": match_score,
                    "matching_skills": self._get_matching_skills(
                        job.required_skills,
                        candidate.resume.skills
                    ),
                    "missing_skills": self._get_missing_skills(
                        job.required_skills,
                        candidate.resume.skills
                    )
                })
                
        return sorted(matches, key=lambda x: x["match_score"], reverse=True)

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