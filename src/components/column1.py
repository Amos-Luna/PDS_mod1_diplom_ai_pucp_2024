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
                
                st.session_state.plot_analytics_paths = []
                st.session_state.plot_analytics_paths.append(plot_temporal_evolution_magnitude(st.session_state.processed_data['df_temp_mag']))
                st.session_state.plot_analytics_paths.append(plot_temporal_evolution_profundidad(st.session_state.processed_data['df_temp_prof']))
                st.session_state.plot_analytics_paths.append(plot_histogram_of_magnitud(st.session_state.processed_data['df_histogram_magnitud']))

                st.subheader('Evolución Temporal de la Magnitud Promedio por Año')
                st.image(st.session_state.plot_analytics_paths[0], use_container_width=True)

                st.subheader('Evolución Temporal de la Profundidad Promedio por Año')
                st.image(st.session_state.plot_analytics_paths[1], use_container_width=True)

                st.subheader('Histograma de los Sismos Ocurridos en términos de Magnitud')
                st.image(st.session_state.plot_analytics_paths[2], use_container_width=True)