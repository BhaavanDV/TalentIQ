from typing import List, Optional, Dict, Any
from fastapi import UploadFile, HTTPException
import aiofiles
import os
from datetime import datetime
from sqlalchemy.orm import Session
from app.schemas.resume import ResumeCreate, ResumeUpdate, Resume
from app.repositories.resume_repository import ResumeRepository
from app.services.file_service import FileService
from app.services.text_extraction_service import TextExtractionService
from app.services.skills_extraction_service import SkillsExtractionService
from app.core.config import settings

class ResumeService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ResumeRepository()
        self.file_service = FileService()
        self.text_extractor = TextExtractionService()
        self.skills_extractor = SkillsExtractionService()

    async def create_resume(self, user_id: int, file: UploadFile) -> Resume:
        """
        Create a new resume entry and process the uploaded file
        """
        # Validate file
        if not self.file_service.is_valid_resume(file):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Please upload PDF or DOCX files only."
            )

        # Create resume entry
        resume_in = ResumeCreate(
            user_id=user_id,
            filename=file.filename,
            mime_type=file.content_type,
            file_size=0  # Will be updated after saving
        )
        
        # Save file
        file_path = await self.file_service.save_resume_file(file)
        resume_in.file_size = os.path.getsize(file_path)
        
        # Create database entry
        resume = self.repository.create(self.db, obj_in=resume_in)
        
        # Process resume asynchronously
        await self._process_resume(resume.id, file_path)
        
        return resume

    async def _process_resume(self, resume_id: int, file_path: str) -> None:
        """
        Process the resume file to extract text and information
        """
        try:
            # Extract text
            text = await self.text_extractor.extract_text(file_path)
            
            # Extract skills and other information
            skills = await self.skills_extractor.extract_skills(text)
            
            # Update resume with extracted information
            resume_update = ResumeUpdate(
                processed_text=text,
                skills=skills,
                status="processed"
            )
            
            self.repository.update(self.db, id=resume_id, obj_in=resume_update)
            
        except Exception as e:
            # Update resume with error status
            error_update = ResumeUpdate(
                status="error",
                error_message=str(e)
            )
            self.repository.update(self.db, id=resume_id, obj_in=error_update)
            raise

    def get(self, resume_id: int) -> Optional[Resume]:
        """
        Get a resume by ID
        """
        return self.repository.get(self.db, resume_id)

    def get_user_resumes(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Resume]:
        """
        Get all resumes for a specific user
        """
        return self.repository.get_multi(
            self.db,
            skip=skip,
            limit=limit,
            filters={"user_id": user_id}
        )

    def update(
        self,
        resume_id: int,
        resume_in: ResumeUpdate
    ) -> Resume:
        """
        Update a resume
        """
        resume = self.repository.get(self.db, resume_id)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        return self.repository.update(self.db, id=resume_id, obj_in=resume_in)

    def delete(self, resume_id: int) -> None:
        """
        Delete a resume and its associated file
        """
        resume = self.repository.get(self.db, resume_id)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        # Delete file
        if resume.file_path:
            self.file_service.delete_file(resume.file_path)
        
        # Delete database entry
        self.repository.delete(self.db, id=resume_id)