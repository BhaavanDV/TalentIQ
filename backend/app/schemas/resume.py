from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ResumeStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    PROCESSED = "processed"
    ERROR = "error"

class Education(BaseModel):
    degree: str
    institution: str
    field_of_study: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    gpa: Optional[float] = None

class Experience(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    description: Optional[str] = None
    skills_used: List[str] = []

class ResumeBase(BaseModel):
    user_id: int

class ResumeCreate(ResumeBase):
    filename: str
    mime_type: str
    file_size: int

class ResumeUpdate(BaseModel):
    processed_text: Optional[str] = None
    skills: Optional[List[str]] = None
    experience: Optional[List[Experience]] = None
    education: Optional[List[Education]] = None
    metadata: Optional[Dict[str, Any]] = None

class ResumeInDBBase(ResumeBase):
    id: int
    filename: str
    status: ResumeStatus
    file_path: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class Resume(ResumeInDBBase):
    skills: Optional[List[str]] = []
    experience: Optional[List[Experience]] = []
    education: Optional[List[Education]] = []
    metadata: Optional[Dict[str, Any]] = {}

class ResumeInDB(ResumeInDBBase):
    original_text: Optional[str] = None
    processed_text: Optional[str] = None