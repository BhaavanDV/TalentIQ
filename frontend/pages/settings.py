import streamlit as st
from utils.ui import show_success_message

def settings_page():
    """Settings page with configuration options"""
    st.title("Settings")
    
    # API Configuration
    st.subheader("API Configuration")
    api_url = st.text_input("API URL", value="http://localhost:8000")
    
    # Application Settings
    st.subheader("Application Settings")
    col1, col2 = st.columns(2)
    
    with col1:
        st.selectbox(
            "Theme",
            ["Light", "Dark", "System Default"],
            index=2
        )
        
        st.selectbox(
            "Language",
            ["English", "Spanish", "French", "German"],
            index=0
        )
    
    with col2:
        st.number_input(
            "Results per page",
            min_value=5,
            max_value=50,
            value=10
        )
        
        st.selectbox(
            "Date Format",
            ["MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD"],
            index=2
        )
    
    # Notification Settings
    st.subheader("Notification Settings")
    st.checkbox("Email notifications", value=True)
    st.checkbox("Browser notifications", value=True)
    st.checkbox("Mobile push notifications", value=False)
    
    # Export/Import Settings
    st.subheader("Data Management")
    col1, col2 = st.columns(2)
    
    with col1:
        st.button("Export Settings")
        st.button("Export Data")
    
    with col2:
        st.file_uploader("Import Settings", type=["json"])
        st.button("Clear All Data")
    
    # Save Settings
    if st.button("Save Settings", type="primary"):
        show_success_message("Settings saved successfully")