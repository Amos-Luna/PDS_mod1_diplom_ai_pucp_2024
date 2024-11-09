import streamlit as st
from pydantic import BaseModel, ConfigDict
from models.data_processor import DataProcessor
from models.geo_data_processor import GeoDataProcessor
from models.histogram_processor import HistogramProcessor
from models.map_processor import MapProcessor
from models.temporal_evolution import TemporalEvolution
from utils import data_loader


class Sidebar(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def render(self):
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
                    st.session_state.df, st.session_state.gdf_peru = data_loader(uploaded_dataset, uploaded_geojson)
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
                        data_processor = DataProcessor(df=st.session_state.df)
                        temporal_evolution = TemporalEvolution(processor=data_processor)             
                        geo_processor = GeoDataProcessor(df=st.session_state.df)
                        map_processor = MapProcessor(df=st.session_state.df)
                        histogram_processor = HistogramProcessor(df=st.session_state.df)
                        
                        st.session_state.processed_data = {
                            'df_temp_mag': temporal_evolution.magnitude_evolution(start_year, end_year),
                            'df_temp_prof': temporal_evolution.profundidad_evolution(start_year, end_year),
                            'gdf_limits_peru': geo_processor.make_choropleth(start_year, end_year),
                            'country_map': map_processor.process_folium_map(start_year, end_year),
                            'df_histogram_magnitud': histogram_processor.process_histogram_magnitude(start_year, end_year)

                        }
                        st.success("Procesamiento completado")
            else:
                st.warning("Por favor, sube ambos archivos para continuar.")