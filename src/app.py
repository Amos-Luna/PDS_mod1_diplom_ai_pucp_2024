import streamlit as st
import pandas as pd
import geopandas as gpd
import altair as alt
from preprocessor import (
    temporal_evolution_magnitude, 
    temporal_evolution_profundidad,
    make_choropleth,
    process_folium_map,
    process_histogram_magnitude
)
from utils import (
    data_loader,
    plot_temporal_evolution_magnitude, 
    plot_temporal_evolution_profundidad,
    plot_choropleth_peru,
    plot_histogram_of_magnitud
)
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
import warnings
warnings.filterwarnings('ignore')


alt.themes.enable('default')
plt.style.use('dark_background')
st.set_page_config(
    page_title="Dashboard de Sismos en Perú",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)


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

st.markdown('<h1 class="main-title">Dashboard de Sismos en Perú</h1>', unsafe_allow_html=True)


if 'df' not in st.session_state:
    st.session_state.df = None
if 'gdf_peru' not in st.session_state:
    st.session_state.gdf_peru = None
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None


with st.sidebar:
    st.title('Carga los Archivos correspondientes')
    
    uploaded_dataset = st.file_uploader(
        "Cargar Dataset de Sismos (Excel)", 
        type=["xlsx"], 
        key="dataset_uploader"
    )
    
    uploaded_geojson = st.file_uploader(
        "Cargar Archivo GeoJSON del Mapa de Perú", 
        type=["geojson"], 
        key="geojson_uploader"
    )

    if uploaded_dataset is not None and uploaded_geojson is not None:
        if st.session_state.df is None or st.session_state.gdf_peru is None:
            st.session_state.df, st.session_state.gdf_peru = data_loader(
                uploaded_dataset, 
                uploaded_geojson
            )
            st.success("Archivos cargados correctamente")

        if st.session_state.df is not None:
            st.title('Selecciona Rango de Años a Analizar')
            year_list = sorted(list(st.session_state.df['YEAR'].unique()))[::-1]
            
            start_year = st.selectbox(
                '**Selecciona Año de Inicio**', 
                year_list, 
                index=len(year_list)-1, 
                key="start_year"
            )
            
            end_year = st.selectbox(
                '**Selecciona Año Final**', 
                year_list, 
                index=0,
                key="end_year"
            )

            if st.button('Iniciar Procesamiento', key="process_button"):
                st.session_state.processed_data = {
                    'df_temp_mag': temporal_evolution_magnitude(st.session_state.df, start_year, end_year),
                    'df_temp_prof': temporal_evolution_profundidad(st.session_state.df, start_year, end_year),
                    'gdf_limits_peru': make_choropleth(st.session_state.df, start_year, end_year),
                    'country_map': process_folium_map(st.session_state.df, start_year, end_year),
                    'histogram_magnitud': process_histogram_magnitude(st.session_state.df, start_year, end_year)
                }
                st.success("Procesamiento completado")
    else:
        st.warning("Por favor, sube ambos archivos para continuar.")


if st.session_state.processed_data is not None:
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        with st.container():
            st.subheader('Evolución Temporal de la Magnitud Promedio por Año')
            plt.figure(figsize=(10, 5))
            fig1 = plot_temporal_evolution_magnitude(st.session_state.processed_data['df_temp_mag'])
            st.pyplot(fig1, use_container_width=True)
            plt.close()
            
            st.subheader('Evolución Temporal de la Profundidad Promedio por Año')
            plt.figure(figsize=(10, 6))
            fig2 = plot_temporal_evolution_profundidad(st.session_state.processed_data['df_temp_prof'])
            st.pyplot(fig2, use_container_width=True)
            plt.close()
            
            st.subheader('Histograma de los Sismos Ocurridos en terminos de Magnitud')
            plt.figure(figsize=(10, 6))
            fig3= plot_histogram_of_magnitud(st.session_state.processed_data['histogram_magnitud'])
            st.pyplot(fig3, use_container_width=True)
            plt.close()
            

    with col2:
        with st.container():
            try:
                st.subheader('Mapa de Sismos en Perú - HeatMap')
                folium_map = st.session_state.processed_data['country_map']
                if folium_map is not None:
                    st_folium(
                        folium_map,
                        width=None,
                        height=450,
                        returned_objects=["last_active_drawing"],
                        use_container_width=True
                    )
                else:
                    st.warning("No se pudo cargar el mapa")
            except Exception as e:
                st.error(f"Error al cargar el mapa: {str(e)}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            try:
                st.subheader('Mapa de Sismos en Perú - Selected Points')
                plt.figure(figsize=(8, 12))
                fig3 = plot_choropleth_peru(
                    st.session_state.df,
                    st.session_state.gdf_peru,
                    st.session_state.processed_data['gdf_limits_peru']
                )
                st.pyplot(fig3, use_container_width=True)
                plt.close()
            except Exception as e:
                st.error(f"Error al cargar el mapa de puntos: {str(e)}")