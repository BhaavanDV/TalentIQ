from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Float, Enum, JSON, ARRAY
from sqlalchemy.orm import relationship
import enum
from app.db.base_class import Base

class ResumeStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    PROCESSED = "processed"
    ERROR = "error"

class Resume(Base):
    __tablename__ = "resumes"

    # Basic Info
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    mime_type = Column(String(100), nullable=False)
    file_size = Column(Integer, nullable=False)
    
    # Processing Status
    status = Column(Enum(ResumeStatus), default=ResumeStatus.PENDING)
    error_message = Column(Text, nullable=True)
    
    # Extracted Content
    original_text = Column(Text)
    processed_text = Column(Text)
    skills = Column(ARRAY(String))
    experience = Column(JSON)  # List of work experiences
    education = Column(JSON)   # List of educational qualifications
    
    # Metadata
    metadata = Column(JSON)    # Additional extracted information
    
    # Relationships
    user = relationship("User", back_populates="resumes")
    evaluations = relationship("Evaluation", back_populates="resume")