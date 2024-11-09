import streamlit as st
import matplotlib.pyplot as plt
from pydantic import BaseModel, ConfigDict
from utils import (
    plot_temporal_evolution_magnitude, 
    plot_temporal_evolution_profundidad, 
    plot_histogram_of_magnitud
)


class Column1(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def render(self):
        if st.session_state.processed_data is not None:
            with st.container():
                st.subheader('Evolución Temporal de la Magnitud Promedio por Año')
                plt.figure(figsize=(10, 7))
                fig1 = plot_temporal_evolution_magnitude(st.session_state.processed_data['df_temp_mag'])
                st.pyplot(fig1, use_container_width=True)
                plt.close()

                st.subheader('Evolución Temporal de la Profundidad Promedio por Año')
                plt.figure(figsize=(10, 7))
                fig2 = plot_temporal_evolution_profundidad(st.session_state.processed_data['df_temp_prof'])
                st.pyplot(fig2, use_container_width=True)
                plt.close()

                st.subheader('Histograma de los Sismos Ocurridos en terminos de Magnitud')
                plt.figure(figsize=(10, 7))
                fig3 = plot_histogram_of_magnitud(st.session_state.processed_data['df_histogram_magnitud'])
                st.pyplot(fig3, use_container_width=True)
                plt.close()