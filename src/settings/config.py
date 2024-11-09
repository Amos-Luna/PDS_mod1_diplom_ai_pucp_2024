import streamlit as st


def set_page_config():
    """Configura la página de Streamlit"""
    st.set_page_config(
        page_title="Dashboard de Sismos en Perú",
        page_icon="🇵🇪",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def set_markdown():
    """Configura los estilos y títulos de la página"""
    st.markdown("""
        <style>
        .main-title {
            text-align: center;
            padding: 1rem 0;
            margin-bottom: 2rem;
        }
        .stPlot {
            margin-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-title"> 🇵🇪 Dashboard de Sismos en Perú 🇵🇪 </h1>', unsafe_allow_html=True)