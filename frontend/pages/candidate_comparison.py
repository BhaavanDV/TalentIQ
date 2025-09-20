import streamlit as st
from utils.api import APIClient
from utils.ui import create_card, create_status_badge, show_success_message
from utils.visualizations import create_timeline_chart
import pandas as pd
from datetime import datetime, timedelta

def candidate_comparison_page():
    st.title("Candidate Comparison")
    
    api_client = APIClient()
    
    # Sidebar filters
    st.sidebar.subheader("Comparison Settings")
    job_position = st.sidebar.selectbox(
        "Job Position",
        ["Software Engineer", "Data Scientist", "DevOps Engineer", "Product Manager"]
    )
    
    comparison_criteria = st.sidebar.multiselect(
        "Comparison Criteria",
        ["Skills Match", "Experience", "Education", "Cultural Fit", "Technical Assessment"],
        default=["Skills Match", "Experience"]
    )
    
    # Main content
    st.subheader("Select Candidates")
    col1, col2 = st.columns(2)
    
    with col1:
        candidate1 = st.selectbox("First Candidate", ["John Doe", "Jane Smith", "Bob Wilson"])
    
    with col2:
        candidate2 = st.selectbox("Second Candidate", ["Jane Smith", "John Doe", "Bob Wilson"])
    
    if st.button("Compare Candidates"):
        # Simulated comparison data
        comparison_data = {
            "candidates": {
                "John Doe": {
                    "skills_match": 85,
                    "experience": 5,
                    "education": "Master's",
                    "cultural_fit": 90,
                    "technical_score": 88
                },
                "Jane Smith": {
                    "skills_match": 92,
                    "experience": 7,
                    "education": "PhD",
                    "cultural_fit": 85,
                    "technical_score": 95
                },
                "Bob Wilson": {
                    "skills_match": 78,
                    "experience": 3,
                    "education": "Bachelor's",
                    "cultural_fit": 95,
                    "technical_score": 82
                }
            }
        }
        
        # Display comparison
        st.write("### Comparison Results")
        
        comparison_df = pd.DataFrame({
            "Criteria": ["Skills Match", "Experience (years)", "Education", "Cultural Fit", "Technical Score"],
            candidate1: [
                f"{comparison_data['candidates'][candidate1]['skills_match']}%",
                comparison_data['candidates'][candidate1]['experience'],
                comparison_data['candidates'][candidate1]['education'],
                f"{comparison_data['candidates'][candidate1]['cultural_fit']}%",
                f"{comparison_data['candidates'][candidate1]['technical_score']}%"
            ],
            candidate2: [
                f"{comparison_data['candidates'][candidate2]['skills_match']}%",
                comparison_data['candidates'][candidate2]['experience'],
                comparison_data['candidates'][candidate2]['education'],
                f"{comparison_data['candidates'][candidate2]['cultural_fit']}%",
                f"{comparison_data['candidates'][candidate2]['technical_score']}%"
            ]
        })
        
        st.table(comparison_df)
        
        # Radar Chart for Visual Comparison
        import plotly.graph_objects as go
        
        categories = ['Skills Match', 'Experience', 'Cultural Fit', 'Technical Score']
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=[
                comparison_data['candidates'][candidate1]['skills_match'],
                comparison_data['candidates'][candidate1]['experience'] * 10,
                comparison_data['candidates'][candidate1]['cultural_fit'],
                comparison_data['candidates'][candidate1]['technical_score']
            ],
            theta=categories,
            fill='toself',
            name=candidate1
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=[
                comparison_data['candidates'][candidate2]['skills_match'],
                comparison_data['candidates'][candidate2]['experience'] * 10,
                comparison_data['candidates'][candidate2]['cultural_fit'],
                comparison_data['candidates'][candidate2]['technical_score']
            ],
            theta=categories,
            fill='toself',
            name=candidate2
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Candidate Comparison Radar Chart"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations
        st.write("### Recommendations")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**{candidate1}**")
            st.markdown("""
            - Strong technical skills
            - Consider leadership training
            - Good cultural fit
            """)
        
        with col2:
            st.write(f"**{candidate2}**")
            st.markdown("""
            - Excellent experience
            - Higher education advantage
            - Superior technical score
            """)
        
        # Final Score
        st.write("### Final Score")
        final_scores = {
            candidate1: sum([
                comparison_data['candidates'][candidate1]['skills_match'],
                comparison_data['candidates'][candidate1]['experience'] * 10,
                comparison_data['candidates'][candidate1]['cultural_fit'],
                comparison_data['candidates'][candidate1]['technical_score']
            ]) / 4,
            candidate2: sum([
                comparison_data['candidates'][candidate2]['skills_match'],
                comparison_data['candidates'][candidate2]['experience'] * 10,
                comparison_data['candidates'][candidate2]['cultural_fit'],
                comparison_data['candidates'][candidate2]['technical_score']
            ]) / 4
        }
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(candidate1, f"{final_scores[candidate1]:.1f}%")
        with col2:
            st.metric(candidate2, f"{final_scores[candidate2]:.1f}%")

if __name__ == "__main__":
    candidate_comparison_page()