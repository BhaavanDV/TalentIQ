import streamlit as st
import requests
import pandas as pd
from pathlib import Path
import json
from datetime import datetime

# Configure page settings
st.set_page_config(
    page_title="TalentIQ - Smart Resume Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_URL = "http://localhost:8000"

# Load modern color scheme
with open("styles/modern.css") as f:
    st.markdown(f.read(), unsafe_allow_html=True)

# Additional theme configuration
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 100%);
    }
    .reportview-container {
        background: transparent;
    }
    .main > div {
        background-color: transparent;
    }
    </style>
""", unsafe_allow_html=True)

def sidebar_menu():
    """Create the sidebar navigation menu"""
    st.sidebar.title("TalentIQ")
    menu_options = {
        "Dashboard": "📊",
        "Resume Upload": "📁",
        "Resume Analysis": "🔍",
        "Job Listings": "💼",
        "Candidate Comparison": "⚖️",
        "Analytics": "📈",
        "Settings": "⚙️"
    }
    
    selected = st.sidebar.selectbox(
        "Navigation",
        list(menu_options.keys()),
        format_func=lambda x: f"{menu_options[x]} {x}",
        key="nav_menu"
    )
    return selected

def dashboard_page():
    """Main dashboard page"""
    st.title("TalentIQ Dashboard")
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Resumes", value="0", delta="↑ New")
    with col2:
        st.metric(label="Active Jobs", value="0", delta="")
    with col3:
        st.metric(label="Matches Found", value="0", delta="")
    
    # Recent Activity
    st.subheader("Recent Activity")
    st.table(pd.DataFrame({
        "Date": [],
        "Activity": [],
        "Status": []
    }))

def upload_resume_page():
    """Resume upload page"""
    st.title("Upload Resume")
    
    # Create upload container
    with st.container():
        st.markdown("""
            <div class="upload-box">
                <h3>Drag and Drop Resume</h3>
                <p>Supported formats: PDF, DOCX</p>
            </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'docx'], label_visibility="collapsed")
        
        if uploaded_file:
            try:
                files = {"file": uploaded_file}
                response = requests.post(f"{API_URL}/api/v1/resumes/", files=files)
                
                if response.status_code == 200:
                    st.success("Resume uploaded successfully!")
                    st.json(response.json())
                else:
                    st.error("Failed to upload resume")
            except Exception as e:
                st.error(f"Error: {str(e)}")

def job_listings_page():
    """Job listings page"""
    st.title("Job Listings")
    
    # Filters
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("Search Jobs", placeholder="Enter keywords...", key="job_search")
    with col2:
        filter_status = st.selectbox("Status", ["All", "Active", "Closed"], key="job_status")
    
    try:
        response = requests.get(f"{API_URL}/api/v1/jobs/")
        if response.status_code == 200:
            jobs = response.json()
            for job in jobs:
                with st.expander(f"{job['title']} - {job['status']}"):
                    st.write(f"**Description:** {job['description']}")
                    st.button("Apply", key=f"apply_{job['id']}")
    except Exception as e:
        st.error(f"Error fetching jobs: {str(e)}")

def analytics_page():
    """Analytics and insights page"""
    st.title("Analytics & Insights")
    
    # Sample visualization
    chart_data = pd.DataFrame({
        "date": pd.date_range(start="2025-01-01", periods=10),
        "applications": [0] * 10
    })
    
    st.line_chart(chart_data.set_index("date"))
    
    # Skills distribution
    st.subheader("Top Skills in Demand")
    skills_data = pd.DataFrame({
        "Skill": ["Python", "Java", "JavaScript"],
        "Demand": [75, 65, 55]
    })
    st.bar_chart(skills_data.set_index("Skill"))

def main():
    """Main application entry point"""
    selected_page = sidebar_menu()
    
    # Page routing with lazy imports
    if selected_page == "Resume Analysis":
        from pages.resume_analysis import resume_analysis_page
        resume_analysis_page()
    elif selected_page == "Dashboard":
        dashboard_page()
    elif selected_page == "Resume Upload":
        upload_resume_page()
    elif selected_page == "Job Listings":
        job_listings_page()
    elif selected_page == "Candidate Comparison":
        st.title("Candidate Comparison")
        st.info("Candidate comparison feature coming soon!")
    elif selected_page == "Analytics":
        analytics_page()
    elif selected_page == "Settings":
        st.title("Settings")
        st.info("Settings page coming soon!")

if __name__ == "__main__":
    main()