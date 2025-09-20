import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any

def create_skill_chart(skills_data: List[Dict[str, Any]]) -> go.Figure:
    """Create a horizontal bar chart for skills"""
    df = pd.DataFrame(skills_data)
    fig = px.bar(
        df,
        x="score",
        y="skill",
        orientation="h",
        title="Skills Assessment",
        labels={"score": "Match Score (%)", "skill": "Skill"},
        color="score",
        color_continuous_scale="viridis",
    )
    fig.update_layout(
        showlegend=False,
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig

def create_match_gauge(match_score: float) -> go.Figure:
    """Create a gauge chart for overall match score"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = match_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Overall Match Score"},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 30], 'color': "red"},
                {'range': [30, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "green"}
            ],
        }
    ))
    fig.update_layout(height=250)
    return fig

def create_timeline_chart(activity_data: List[Dict[str, Any]]) -> go.Figure:
    """Create a timeline chart for activities"""
    df = pd.DataFrame(activity_data)
    fig = px.line(
        df,
        x="date",
        y="value",
        title="Activity Timeline",
        labels={"value": "Count", "date": "Date"},
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Number of Activities",
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig

def format_metrics_grid(metrics: Dict[str, Any]) -> None:
    """Display metrics in a grid layout"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label=metrics.get("label1", "Metric 1"),
            value=metrics.get("value1", "0"),
            delta=metrics.get("delta1", "0")
        )
    
    with col2:
        st.metric(
            label=metrics.get("label2", "Metric 2"),
            value=metrics.get("value2", "0"),
            delta=metrics.get("delta2", "0")
        )
    
    with col3:
        st.metric(
            label=metrics.get("label3", "Metric 3"),
            value=metrics.get("value3", "0"),
            delta=metrics.get("delta3", "0")
        )