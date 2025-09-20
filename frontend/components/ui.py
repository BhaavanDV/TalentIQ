import streamlit as st

def card(title, content, icon=None):
    """Render a styled card component"""
    st.markdown(f"""
        <div class="card mb-4">
            <div class="flex items-center mb-3">
                {f'<span class="text-2xl mr-2">{icon}</span>' if icon else ''}
                <h3 class="text-xl font-semibold">{title}</h3>
            </div>
            <div class="text-gray-300">
                {content}
            </div>
        </div>
    """, unsafe_allow_html=True)

def badge(text, color="blue"):
    """Render a styled badge"""
    st.markdown(f"""
        <span class="badge badge-{color}">
            {text}
        </span>
    """, unsafe_allow_html=True)

def stat_card(label, value, delta=None, help_text=None):
    """Render a styled stat card"""
    delta_html = f"""
        <div class="text-sm {'text-green-400' if float(delta.strip('%+ ')) > 0 else 'text-red-400'}">
            {delta}
        </div>
    """ if delta else ""
    
    help_html = f"""
        <div class="tooltip">
            ❔
            <span class="tooltip-text">{help_text}</span>
        </div>
    """ if help_text else ""
    
    st.markdown(f"""
        <div class="kpi-card">
            <div class="flex justify-between items-center">
                <div class="text-sm text-gray-400">{label}</div>
                {help_html}
            </div>
            <div class="text-2xl font-bold mt-2">{value}</div>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)

def progress_bar(value, max_value=100):
    """Render a styled progress bar"""
    percentage = (value / max_value) * 100
    st.markdown(f"""
        <div class="progress-bar">
            <div class="progress-bar-fill" style="width: {percentage}%"></div>
        </div>
        <div class="text-sm text-gray-400 mt-1">{value}/{max_value}</div>
    """, unsafe_allow_html=True)

def glass_container(content):
    """Render content in a glass-morphism container"""
    st.markdown(f"""
        <div class="glass p-6">
            {content}
        </div>
    """, unsafe_allow_html=True)