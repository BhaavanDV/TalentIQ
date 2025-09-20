from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Float, JSON, ARRAY
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Job(Base):
    __tablename__ = "jobs"

    # Basic Info
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    location = Column(String(255))
    description = Column(Text, nullable=False)
    
    # Requirements
    required_skills = Column(ARRAY(String), nullable=False)
    preferred_skills = Column(ARRAY(String))
    qualifications = Column(JSON)  # Educational requirements
    experience_years = Column(Integer)
    
    # Job Details
    job_type = Column(String(50))  # Full-time, Part-time, Contract
    salary_range = Column(JSON)    # Min and max salary
    industry = Column(String(100))
    
    # Processing
    processed_description = Column(Text)
    metadata = Column(JSON)
    
    # Relationships
    evaluations = relationship("Evaluation", back_populates="job")