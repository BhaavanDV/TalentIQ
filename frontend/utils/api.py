import requests
from typing import Dict, List, Any, Optional
import streamlit as st

class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self._check_server_connection()

    def _check_server_connection(self) -> None:
        try:
            requests.get(f"{self.base_url}/health", timeout=2)
        except requests.exceptions.RequestException:
            st.error("⚠️ Cannot connect to the backend server. Please make sure it's running on " + self.base_url)

    def _handle_response(self, response: requests.Response) -> Dict:
        try:
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
                return {}
        except requests.exceptions.RequestException as e:
            st.error(f"Connection Error: {str(e)}")
            return {}

    def upload_resume(self, file) -> Dict:
        """Upload a resume file to the API"""
        try:
            files = {"file": file}
            response = requests.post(f"{self.base_url}/api/v1/resumes/", files=files)
            return self._handle_response(response)
        except Exception as e:
            st.error(f"Upload Error: {str(e)}")
            return {}

    def get_resumes(self) -> List[Dict]:
        """Get list of all uploaded resumes"""
        try:
            response = requests.get(f"{self.base_url}/api/v1/resumes/")
            return self._handle_response(response)
        except Exception as e:
            st.error(f"Error fetching resumes: {str(e)}")
            return []

    def get_jobs(self, search: Optional[str] = None, status: Optional[str] = None) -> List[Dict]:
        """Get list of jobs with optional filters"""
        try:
            params = {}
            if search:
                params["search"] = search
            if status and status != "All":
                params["status"] = status
            
            response = requests.get(f"{self.base_url}/api/v1/jobs/", params=params)
            return self._handle_response(response)
        except Exception as e:
            st.error(f"Error fetching jobs: {str(e)}")
            return []

    def get_evaluations(self, resume_id: Optional[int] = None) -> List[Dict]:
        """Get resume evaluations"""
        try:
            params = {}
            if resume_id:
                params["resume_id"] = resume_id
            
            response = requests.get(f"{self.base_url}/api/v1/evaluations/", params=params)
            return self._handle_response(response)
        except Exception as e:
            st.error(f"Error fetching evaluations: {str(e)}")
            return []