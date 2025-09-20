from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Float, JSON
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Evaluation(Base):
    __tablename__ = "evaluations"

    # References
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    evaluator_id = Column(Integer, ForeignKey("users.id"))
    
    # Scores
    overall_score = Column(Float, nullable=False)
    skills_score = Column(Float, nullable=False)
    experience_score = Column(Float, nullable=False)
    education_score = Column(Float, nullable=False)
    
    # Detailed Results
    matching_skills = Column(JSON)      # List of matched skills
    missing_skills = Column(JSON)       # List of missing required skills
    skill_suggestions = Column(JSON)    # Suggested skills to learn
    
    # Analysis
    strengths = Column(JSON)            # Key strengths identified
    weaknesses = Column(JSON)           # Areas for improvement
    recommendations = Column(Text)      # Detailed recommendations
    
    # Verdict
    suitability = Column(String(50))    # High, Medium, Low
    confidence_score = Column(Float)    # Confidence in the evaluation
    
    # Relationships
    resume = relationship("Resume", back_populates="evaluations")
    job = relationship("Job", back_populates="evaluations")
    evaluator = relationship("User", back_populates="evaluations")