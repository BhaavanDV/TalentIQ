import os
from typing import List
from fastapi import HTTPException, UploadFile
import aiofiles
from datetime import datetime
from app.core.config import settings

class FileService:
    ALLOWED_MIME_TYPES = [
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ]
    
    def is_valid_resume(self, file: UploadFile) -> bool:
        """
        Validate if the uploaded file is of an acceptable type
        """
        return file.content_type in self.ALLOWED_MIME_TYPES

    async def save_resume_file(self, file: UploadFile) -> str:
        """
        Save an uploaded resume file to the configured storage location
        Returns the file path where the file was saved
        """
        # Create directory if it doesn't exist
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(settings.UPLOAD_DIR, filename)
        
        # Save file
        try:
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
            return file_path
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error saving file: {str(e)}"
            )

    def delete_file(self, file_path: str) -> None:
        """
        Delete a file from storage
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error deleting file: {str(e)}"
            )

    def get_file_size(self, file_path: str) -> int:
        """
        Get the size of a file in bytes
        """
        try:
            return os.path.getsize(file_path)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error getting file size: {str(e)}"
            )