from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class SuitabilityLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class SkillMatch(BaseModel):
    skill: str
    required: bool
    match_score: float
    context: Optional[str] = None

class EvaluationBase(BaseModel):
    resume_id: int
    job_id: int

class EvaluationCreate(EvaluationBase):
    evaluator_id: int
    overall_score: float
    skills_score: float
    experience_score: float
    education_score: float
    suitability: SuitabilityLevel

class EvaluationUpdate(BaseModel):
    overall_score: Optional[float] = None
    skills_score: Optional[float] = None
    experience_score: Optional[float] = None
    education_score: Optional[float] = None
    matching_skills: Optional[List[SkillMatch]] = None
    missing_skills: Optional[List[str]] = None
    recommendations: Optional[str] = None
    suitability: Optional[SuitabilityLevel] = None

class EvaluationInDBBase(EvaluationBase):
    id: int
    evaluator_id: int
    overall_score: float
    skills_score: float
    experience_score: float
    education_score: float
    suitability: SuitabilityLevel
    created_at: datetime
    
    class Config:
        from_attributes = True

class Evaluation(EvaluationInDBBase):
    matching_skills: List[SkillMatch] = []
    missing_skills: List[str] = []
    skill_suggestions: List[str] = []
    strengths: List[str] = []
    weaknesses: List[str] = []
    recommendations: Optional[str] = None
    confidence_score: float