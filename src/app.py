import streamlit as st
import pandas as pd
from preprocessor import preprocess_data
from utils import plot_temporal_evolution


path = "data/Catalogo1960_2023.xlsx"
df =  pd.read_excel(path)


st.sidebar.header('Filtros de Datos')
start_date = st.sidebar.date_input('Fecha de inicio', pd.to_datetime('1960-01-01'))
end_date = st.sidebar.date_input('Fecha de fin', pd.to_datetime('1960-12-31'))
min_magnitude = st.sidebar.slider('Nivel de Magnitud', min_value=0.0, max_value=10.0, value=5.0)
max_depth = st.sidebar.slider('Nivel de Profundidad (km)', min_value=0, max_value=700, value=300)

filtered_df = preprocess_data(df, start_date, end_date, min_magnitude, max_depth)

st.sidebar.write("Datos filtrados", filtered_df)


st.title('Análisis de Sismos')
col1, col2 = st.columns([1, 2])

with col2:
    
    st.subheader('Gráfico de Magnitud a lo largo del tiempo')
    fig1 = plot_temporal_evolution(filtered_df)
    st.pyplot(fig1)