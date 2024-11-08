import streamlit as st
import pandas as pd
import geopandas as gpd
import altair as alt
from preprocessor import (
    read_dataset, 
    read_shapefile,
    temporal_evolution_magnitude, 
    temporal_evolution_profundidad,
    make_choropleth
)
from utils import (
    plot_temporal_evolution_magnitude, 
    plot_temporal_evolution_profundidad,
    plot_choropleth_peru
)
import matplotlib.pyplot as plt


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


path_dataset = "data/Catalogo1960_2023.xlsx"
path_geojson_peru = "data/peru_departamental_simple.geojson" 

df: pd.DataFrame = read_dataset(path_dataset)
gdf_peru: gpd.GeoDataFrame = read_shapefile(path_geojson_peru)

with st.sidebar:
    st.title('Selecciona Rango de Años a Analizar')
    year_list = list(df.year.unique())[::-1]
    start_year = st.selectbox('**Selecciona Año Inicio**', year_list, index=len(year_list)-1)
    end_year = st.selectbox('**Selecciona Año Final**', year_list, index=len(year_list)-1)
    

df_temp_mag = temporal_evolution_magnitude(df, start_year, end_year)
df_temp_prof = temporal_evolution_profundidad(df, start_year, end_year)
gdf_limits_peru = make_choropleth(df, start_year, end_year)


col1, col2 = st.columns([1.2, 1])
with col1:
    with st.container():
        st.subheader('Evolución Temporal de la Magnitud Promedio por Año')
        plt.figure(figsize=(10, 5))
        fig1 = plot_temporal_evolution_magnitude(df_temp_mag)
        st.pyplot(fig1, use_container_width=True)
        plt.close()
        
        st.subheader('Evolución Temporal de la Profundidad Promedio por Año')
        plt.figure(figsize=(10, 6))
        fig2 = plot_temporal_evolution_profundidad(df_temp_prof)
        st.pyplot(fig2, use_container_width=True)
        plt.close()

with col2:
    with st.container():
        st.subheader('Mapa de Sismos en Perú')
        plt.figure(figsize=(8, 12))
        fig3 = plot_choropleth_peru(df, gdf_peru, gdf_limits_peru)
        st.pyplot(fig3, use_container_width=True)
        plt.close()