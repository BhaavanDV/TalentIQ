from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Float, Enum, Boolean, JSON, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"

    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # Relationships
    resumes = relationship("Resume", back_populates="user")
    evaluations = relationship("Evaluation", back_populates="evaluator")