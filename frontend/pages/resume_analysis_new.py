import streamlit as st
from utils.api import APIClient
from utils.ui import create_card, show_success_message, show_error_message
from utils.visualizations import create_skill_chart, create_match_gauge
import pandas as pd
from typing import Dict, Any
import time

def show_analysis_results():
    with st.spinner("Analyzing resume..."):
        analysis_results = {
            "skills": [
                {"skill": "Python", "score": 85},
                {"skill": "Machine Learning", "score": 75},
                {"skill": "Data Analysis", "score": 90},
                {"skill": "Cloud Computing", "score": 70}
            ],
            "overall_match": 82
        }
        st.write("### Skills Assessment")
        st.plotly_chart(create_skill_chart(analysis_results["skills"]))
        st.write("### Overall Match")
        st.plotly_chart(create_match_gauge(analysis_results["overall_match"]))

def resume_analysis_page():
    st.title("Resume Analysis")
    api_client = APIClient()
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Resume List")
        try:
            resumes = api_client.get_resumes()
            if resumes:
                for resume in resumes:
                    with st.expander(f"{resume.get('filename', 'Unnamed Resume')}"):
                        st.write(f"**Uploaded:** {resume.get('uploaded_at', 'Unknown')}")
                        st.write(f"**Size:** {resume.get('size', 0)} bytes")
                        if st.button("Analyze", key=f"analyze_{resume.get('id')}"):
                            show_analysis_results()
            else:
                st.info("No resumes found. Upload a resume to begin analysis.")
        except Exception as e:
            st.error("⚠️ Cannot connect to the server")
            st.info("💡 Make sure the backend server is running (uvicorn app:app --reload)")
    
    with col2:
        st.subheader("Quick Stats")
        try:
            metrics = {
                "Resumes": len(resumes) if 'resumes' in locals() else 0,
                "Match Score": "78%",
                "Skills": "Python, ML"
            }
            for key, value in metrics.items():
                create_card(key, str(value))
        except Exception:
            st.warning("Unable to load statistics")