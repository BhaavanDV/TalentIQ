# -*- coding: utf-8 -*-
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# API Configuration
API_URL = "http://localhost:8000"


def load_resume_data():
    """Load resume data from the API"""
    try:
        response = requests.get(f"{API_URL}/api/v1/resumes/")
        if response.status_code == 200:
            return response.json()
        return []
    except requests.exceptions.ConnectionError:
        st.warning("⚠️ Backend server is not running. Start with: cd backend && uvicorn main:app --reload --port 8000")
        return []
    except Exception as e:
        st.error(f"Error loading resume data: {str(e)}")
        return []


def analyze_skills(resume_text):
    """Analyze skills from resume text"""
    try:
        response = requests.post(
            f"{API_URL}/api/v1/analyze/skills",
            json={"text": resume_text}
        )
        if response.status_code == 200:
            return response.json()
        return {"skills": [], "confidence_scores": []}
    except Exception:
        return {"skills": [], "confidence_scores": []}


def create_skills_chart(skills_data):
    """Create a skills analysis chart"""
    if not skills_data["skills"]:
        return None

    fig = px.bar(
        x=skills_data["skills"],
        y=skills_data["confidence_scores"],
        title="Skills Analysis",
        labels={"x": "Skills", "y": "Confidence Score"},
        color=skills_data["confidence_scores"],
        color_continuous_scale="viridis"
    )
    fig.update_layout(showlegend=False)
    return fig


def create_experience_timeline(resume_data):
    """Create an experience timeline visualization"""
    if not resume_data.get("experience", []):
        return None

    fig = go.Figure()
    for exp in resume_data["experience"]:
        fig.add_trace(go.Scatter(
            x=[exp["start_date"], exp["end_date"]],
            y=[exp["company"]],
            mode="lines+markers",
            name=exp["title"],
            line=dict(width=2),
            marker=dict(size=8)
        ))

    fig.update_layout(
        title="Professional Experience Timeline",
        xaxis_title="Date",
        yaxis_title="Company",
        showlegend=True
    )
    return fig


def resume_analysis_page():
    """Main resume analysis page"""
    st.title("💼 Resume Analysis Dashboard")
    st.markdown("Intelligent Resume Analysis and Matching System")

    # Sidebar filters
    st.sidebar.header("Analysis Filters")
    filter_date = st.sidebar.date_input("Filter by Date", datetime.now())
    filter_skills = st.sidebar.multiselect(
        "Filter by Skills",
        ["Python", "Java", "JavaScript", "Machine Learning", "Data Analysis"]
    )
    filter_experience = st.sidebar.slider(
        "Years of Experience", 0, 20, (0, 20)
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📄 Resume Upload")
        uploaded_file = st.file_uploader(
            "Upload Resume (PDF, DOCX)", type=["pdf", "docx"]
        )

        if uploaded_file:
            with st.spinner("Analyzing resume..."):
                st.success("Resume uploaded successfully!")

                # Mock skills data for now
                sample_skills = {
                    "skills": ["Python", "Java", "AWS", "Docker", "SQL"],
                    "confidence_scores": [0.95, 0.85, 0.78, 0.92, 0.88]
                }

                skills_chart = create_skills_chart(sample_skills)
                if skills_chart:
                    st.plotly_chart(skills_chart, use_container_width=True)

                # KPI Section
                st.subheader("🎯 Key Insights")
                kpi1, kpi2, kpi3 = st.columns(3)
                kpi1.metric("Skills Match", "85%", "+5%")
                kpi2.metric("Experience Score", "8.5/10", "+0.5")
                kpi3.metric("Overall Ranking", "#3", "↑ 2 positions")

    with col2:
        st.subheader("📊 Analytics")

        exp_data = pd.DataFrame({
            "Level": ["Entry", "Mid", "Senior", "Lead"],
            "Count": [10, 25, 15, 5]
        })
        fig = px.pie(exp_data, values="Count", names="Level",
                     title="Experience Level Distribution")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("🌟 Top Skills in Demand")
        skills_demand = pd.DataFrame({
            "Skill": ["Python", "AWS", "React", "SQL", "Docker"],
            "Demand": [95, 88, 82, 78, 75]
        })
        fig = px.bar(skills_demand, x="Skill", y="Demand",
                     title="Skills Demand (%)",
                     color="Demand", color_continuous_scale="viridis")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("💡 Recommendations")
        with st.expander("Skills Development", expanded=True):
            st.markdown("""
            - Strengthen Cloud Computing skills  
            - Add projects showcasing Python expertise  
            - Get certified in AWS or Azure  
            """)
        with st.expander("Resume Improvements"):
            st.markdown("""
            - Add quantifiable achievements  
            - Highlight leadership experience  
            - Include certifications  
            """)


if __name__ == "__main__":
    resume_analysis_page()
