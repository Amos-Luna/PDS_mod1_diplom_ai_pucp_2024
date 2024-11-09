import streamlit as st


def initialize_session_state():
    """Inicializa las variables en session_state si no existen"""
    
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'gdf_peru' not in st.session_state:
        st.session_state.gdf_peru = None
    if 'processed_data' not in st.session_state:
        st.session_state.processed_data = None
    if 'plot_analytics_paths' not in st.session_state:
        st.session_state.plot_analytics_paths = None
    if 'plot_map_paths' not in st.session_state:
        st.session_state.plot_map_paths = None
    if 'openai_api_key' not in st.session_state:
        st.session_state.openai_api_key = None
    if "messages" not in st.session_state:
        st.session_state.messages = None