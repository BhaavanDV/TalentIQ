import re
from typing import List, Set, Dict, Any
import spacy
from spacy.matcher import Matcher
import json
import os
from app.core.config import settings

class SkillsExtractionService:
    def __init__(self):
        # Load spaCy model
        self.nlp = spacy.load("en_core_web_sm")
        self.skills_data = self._load_skills_data()
        self.matcher = self._setup_matcher()

    def _load_skills_data(self) -> Dict[str, List[str]]:
        """
        Load skills data from JSON file
        The file should contain categories of skills with variations
        """
        skills_file = os.path.join(settings.DATA_DIR, "skills.json")
        try:
            with open(skills_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Return empty dict if file not found
            return {}

    def _setup_matcher(self) -> Matcher:
        """
        Set up spaCy matcher with patterns for skills recognition
        """
        matcher = Matcher(self.nlp.vocab)
        
        # Add patterns for each skill and its variations
        for category, skills in self.skills_data.items():
            for skill in skills:
                # Create pattern for exact matches
                pattern = [{"LOWER": skill.lower()}]
                matcher.add(f"SKILL_{skill}", [pattern])
                
                # Add patterns for multi-word skills
                if " " in skill:
                    words = skill.lower().split()
                    pattern = [{"LOWER": word} for word in words]
                    matcher.add(f"SKILL_{skill}_MW", [pattern])
        
        return matcher

    async def extract_skills(self, text: str) -> Dict[str, List[str]]:
    
        doc = self.nlp(text)
        matches = self.matcher(doc)
        
        # Collect unique skills
        found_skills: Dict[str, Set[str]] = {}
        
        for match_id, start, end in matches:
            skill_text = doc[start:end].text
            
            # Find which category this skill belongs to
            for category, skills in self.skills_data.items():
                if any(skill.lower() == skill_text.lower() for skill in skills):
                    if category not in found_skills:
                        found_skills[category] = set()
                    found_skills[category].add(skill_text)
        
        # Convert sets to lists for JSON serialization
        return {
            category: sorted(list(skills))
            for category, skills in found_skills.items()
        }

    async def extract_experience_levels(self, text: str) -> Dict[str, str]:
     
        # Simple pattern matching for years of experience
        experience_patterns = [
            r"(\d+)[\+]?\s*(?:years?|yrs?).+?experience.+?(?:with|in|using)?\s+([A-Za-z0-9#\+]+)",
            r"([A-Za-z0-9#\+]+).+?(\d+)[\+]?\s*(?:years?|yrs?).+?experience"
        ]
        
        experience_levels = {}
        
        for pattern in experience_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match.groups()) == 2:
                    years, skill = match.groups()
                    experience_levels[skill] = f"{years}+ years"
        
        return experience_levels