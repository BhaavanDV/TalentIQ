from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class SalaryRange(BaseModel):
    min: float
    max: float
    currency: str = "USD"
    period: str = "yearly"

class Qualification(BaseModel):
    degree: str
    field: Optional[str] = None
    is_required: bool = True

class JobBase(BaseModel):
    title: str
    company: str
    description: str
    required_skills: List[str]
    preferred_skills: Optional[List[str]] = None
    experience_years: Optional[int] = None

class JobCreate(JobBase):
    location: Optional[str] = None
    job_type: Optional[str] = None
    qualifications: Optional[List[Qualification]] = None
    salary_range: Optional[SalaryRange] = None
    industry: Optional[str] = None

class JobUpdate(JobBase):
    title: Optional[str] = None
    company: Optional[str] = None
    description: Optional[str] = None
    required_skills: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None

class JobInDBBase(JobBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class Job(JobInDBBase):
    location: Optional[str] = None
    job_type: Optional[str] = None
    qualifications: Optional[List[Qualification]] = None
    salary_range: Optional[SalaryRange] = None
    industry: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}