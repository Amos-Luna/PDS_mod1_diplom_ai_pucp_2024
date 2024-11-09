import streamlit as st
from components.sidebar import Sidebar
from components.column1 import Column1
from components.column2 import Column2
from settings.session_state_initializer import initialize_session_state
from settings.config import set_page_config, set_markdown

set_page_config()
set_markdown()
initialize_session_state()

sidebar = Sidebar()
sidebar.render()

col1, col2 = st.columns([1.2, 1])
with col1:
    column1 = Column1()
    column1.render()

with col2:
    column2 = Column2()
    column2.render()