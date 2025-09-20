import streamlit as st
import requests
import pandas as pd
import json

# Configure the app
st.set_page_config(
    page_title="TalentIQ Dashboard",
    page_icon="📊",
    layout="wide"
)

# API Configuration
API_URL = "http://localhost:8000/api/v1"

def main():
    st.title("TalentIQ - Resume Analysis & Job Matching")
    
    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Select a Page",
        ["Dashboard", "Resume Management", "Job Postings", "Evaluations"]
    )
    
    if page == "Dashboard":
        show_dashboard()
    elif page == "Resume Management":
        show_resume_management()
    elif page == "Job Postings":
        show_job_postings()
    elif page == "Evaluations":
        show_evaluations()

def show_dashboard():
    st.header("Dashboard")
    
    # Create columns for metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        try:
            response = requests.get(f"{API_URL}/resumes")
            resume_count = len(response.json()) if response.ok else 0
            st.metric("Total Resumes", resume_count)
        except:
            st.metric("Total Resumes", "N/A")
    
    with col2:
        try:
            response = requests.get(f"{API_URL}/jobs")
            job_count = len(response.json()) if response.ok else 0
            st.metric("Active Jobs", job_count)
        except:
            st.metric("Active Jobs", "N/A")
    
    with col3:
        try:
            response = requests.get(f"{API_URL}/evaluations")
            eval_count = len(response.json()) if response.ok else 0
            st.metric("Total Evaluations", eval_count)
        except:
            st.metric("Total Evaluations", "N/A")

def show_resume_management():
    st.header("Resume Management")
    
    # File upload
    uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
    if uploaded_file:
        files = {"file": uploaded_file}
        try:
            response = requests.post(f"{API_URL}/resumes", files=files)
            if response.ok:
                st.success("Resume uploaded successfully!")
                st.json(response.json())
            else:
                st.error(f"Upload failed: {response.text}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # List existing resumes
    st.subheader("Existing Resumes")
    try:
        response = requests.get(f"{API_URL}/resumes")
        if response.ok:
            resumes = response.json()
            if resumes:
                df = pd.DataFrame(resumes)
                st.dataframe(df)
            else:
                st.info("No resumes found")
    except Exception as e:
        st.error(f"Error loading resumes: {str(e)}")

def show_job_postings():
    st.header("Job Postings")
    
    # Add new job form
    with st.form("new_job"):
        st.subheader("Add New Job")
        title = st.text_input("Job Title")
        description = st.text_area("Job Description")
        required_skills = st.text_input("Required Skills (comma-separated)")
        submit = st.form_submit_button("Create Job")
        
        if submit:
            job_data = {
                "title": title,
                "description": description,
                "required_skills": [s.strip() for s in required_skills.split(",")]
            }
            try:
                response = requests.post(
                    f"{API_URL}/jobs",
                    json=job_data
                )
                if response.ok:
                    st.success("Job posted successfully!")
                else:
                    st.error(f"Failed to post job: {response.text}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # List existing jobs
    st.subheader("Active Jobs")
    try:
        response = requests.get(f"{API_URL}/jobs")
        if response.ok:
            jobs = response.json()
            if jobs:
                df = pd.DataFrame(jobs)
                st.dataframe(df)
            else:
                st.info("No jobs found")
    except Exception as e:
        st.error(f"Error loading jobs: {str(e)}")

def show_evaluations():
    st.header("Resume Evaluations")
    
    # Job selection
    try:
        response = requests.get(f"{API_URL}/jobs")
        if response.ok:
            jobs = response.json()
            if jobs:
                job_titles = [f"{j['title']} (ID: {j['id']})" for j in jobs]
                selected_job = st.selectbox("Select Job", job_titles)
                job_id = int(selected_job.split("ID: ")[-1].rstrip(")"))
                
                # Show matching candidates
                st.subheader("Matching Candidates")
                response = requests.get(f"{API_URL}/evaluations/job/{job_id}")
                if response.ok:
                    evaluations = response.json()
                    if evaluations:
                        df = pd.DataFrame(evaluations)
                        st.dataframe(df)
                    else:
                        st.info("No evaluations found for this job")
            else:
                st.info("No jobs available")
    except Exception as e:
        st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()