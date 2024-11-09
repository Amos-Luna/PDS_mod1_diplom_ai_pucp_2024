import streamlit as st
import matplotlib.pyplot as plt
from components.chatbot import Chatbot
from utils import plot_choropleth_peru
from pydantic import BaseModel, ConfigDict


class Column2(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def render(self):
        if st.session_state.processed_data is not None:
            try:
                with st.container():
                    st.subheader('Ubicación de Sismos en Perú')
                    fig3 = plot_choropleth_peru(st.session_state.df, st.session_state.gdf_peru, st.session_state.processed_data['gdf_limits_peru'])
                    st.pyplot(fig3, use_container_width=True)
                    plt.close()
                    
                    chatbot = Chatbot()
                    chatbot.render()

            except Exception as e:
                st.error(f"Error al cargar el mapa de puntos: {str(e)}")