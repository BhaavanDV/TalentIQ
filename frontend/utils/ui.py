import streamlit as st
from typing import Dict, Any
import json

def load_config() -> Dict[str, Any]:
    """Load application configuration"""
    return {
        "theme_colors": {
            "primary": "#1f77b4",
            "secondary": "#ff7f0e",
            "success": "#2ca02c",
            "danger": "#d62728",
            "warning": "#ffbb00",
        },
        "api_url": "http://localhost:8000",
        "upload_types": ["pdf", "docx"],
        "max_file_size": 5 * 1024 * 1024,  # 5MB
    }

def apply_custom_css() -> None:
    """Apply custom CSS styling"""
    st.markdown("""
        <style>
        .main {
            padding: 1rem;
        }
        .stButton>button {
            width: 100%;
            background-color: var(--primary-color);
            color: white;
        }
        .css-1d391kg {
            padding: 1rem;
        }
        .upload-box {
            border: 2px dashed #cccccc;
            padding: 20px;
            text-align: center;
            border-radius: 10px;
            margin: 1rem 0;
        }
        .metric-card {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .filter-section {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        .job-card {
            border: 1px solid #e0e0e0;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            transition: transform 0.2s;
        }
        .job-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)

def show_success_message(message: str) -> None:
    """Display a styled success message"""
    st.markdown(f"""
        <div style="
            padding: 1rem;
            background-color: #d4edda;
            color: #155724;
            border-radius: 10px;
            margin: 1rem 0;
            text-align: center;
        ">
            ✅ {message}
        </div>
    """, unsafe_allow_html=True)

def show_error_message(message: str) -> None:
    """Display a styled error message"""
    st.markdown(f"""
        <div style="
            padding: 1rem;
            background-color: #f8d7da;
            color: #721c24;
            border-radius: 10px;
            margin: 1rem 0;
            text-align: center;
        ">
            ❌ {message}
        </div>
    """, unsafe_allow_html=True)

def create_card(title: str, content: str, footer: str = None) -> None:
    """Create a styled card component"""
    st.markdown(f"""
        <div style="
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
        ">
            <h3 style="margin-top: 0;">{title}</h3>
            <p>{content}</p>
            {f'<div style="color: #666; font-size: 0.9em;">{footer}</div>' if footer else ''}
        </div>
    """, unsafe_allow_html=True)

def create_status_badge(status: str) -> str:
    """Create a colored status badge"""
    colors = {
        "active": "#28a745",
        "pending": "#ffc107",
        "completed": "#17a2b8",
        "rejected": "#dc3545"
    }
    color = colors.get(status.lower(), "#6c757d")
    
    return f"""
        <span style="
            background-color: {color};
            color: white;
            padding: 0.25rem 0.5rem;
            border-radius: 10px;
            font-size: 0.8em;
        ">
            {status.upper()}
        </span>
    """