from typing import List, Dict, Any
from datetime import datetime
import spacy
import re

class TextExtractionService:
    def __init__(self):
        # Load spaCy model for English
        self.nlp = spacy.load("en_core_web_sm")

    async def extract_text(self, file_path: str) -> str:
        """
        Extract text content from a resume file
        Supports PDF and DOCX formats
        """
        file_ext = file_path.lower().split('.')[-1]
        
        if file_ext == 'pdf':
            return await self._extract_from_pdf(file_path)
        elif file_ext == 'docx':
            return await self._extract_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")

    async def _extract_from_pdf(self, file_path: str) -> str:
        """
        Extract text from PDF files
        """
        try:
            import pdfplumber
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")

    async def _extract_from_docx(self, file_path: str) -> str:
        """
        Extract text from DOCX files
        """
        try:
            from docx import Document
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting text from DOCX: {str(e)}")

    async def extract_sections(self, text: str) -> Dict[str, str]:
        """
        Extract common resume sections like education, experience, etc.
        Returns a dictionary with section names as keys and content as values
        """
        sections = {
            'summary': '',
            'education': '',
            'experience': '',
            'skills': '',
            'projects': '',
            'certifications': ''
        }
        
        # Simple section detection based on common headers
        current_section = None
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if line is a section header
            lower_line = line.lower()
            for section in sections.keys():
                if section in lower_line and len(line) < 50:  # Assume headers are relatively short
                    current_section = section
                    break
                    
            if current_section and line:
                sections[current_section] += line + '\n'
                
        return sections