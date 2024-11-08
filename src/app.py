from constants import CHATBOT_MODEL
import streamlit as st
from openai import OpenAI
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
            fig3= plot_histogram_of_magnitud(st.session_state.processed_data['histogram_magnitud'])
            st.pyplot(fig3, use_container_width=True)
            plt.close()
            

    with col2:
        with st.container():
            try:
                st.subheader('Mapa de Sismos en Perú - Selected Points')
                fig3 = plot_choropleth_peru(
                    st.session_state.df,
                    st.session_state.gdf_peru,
                    st.session_state.processed_data['gdf_limits_peru']
                )
                st.pyplot(fig3, use_container_width=True)
                plt.close()
                
                st.markdown("""
                    <style>
                    .stChatFloatingInputContainer {
                        position: sticky !important;
                        bottom: 0 !important;
                        background-color: #0E1117 !important;
                        padding: 1rem 0 !important;
                    }
                    .stChatMessage {
                        background-color: #262730 !important;
                    }
                    .chat-container {
                        display: flex;
                        flex-direction: column;
                        height: 600px;
                        overflow-y: auto;
                        padding-bottom: 100px;
                    }
                    .chat-container > div {
                        flex: 0 0 auto;
                    }
                    </style>
                """, unsafe_allow_html=True)

                openai_api_key = st.text_input("**INSERT YOUR OPENAI_API_KEY** 👇", key="chatbot_api_key", type="password")

                if "messages" not in st.session_state:
                    st.session_state.messages = [{"role": "assistant", "content": "¡Hola! ¿En qué puedo ayudarte hoy?"}]

                
                messages_container = st.container(height=700)
                with messages_container:
                    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
                    
                    for msg in st.session_state.messages:
                        with st.chat_message(msg["role"]):
                            st.write(msg["content"])
                    st.markdown('</div>', unsafe_allow_html=True)

                prompt = st.chat_input("Escribe tu mensaje aquí...")
                if prompt:
                    if not openai_api_key:
                        st.info("Por favor, añade tu API key de OpenAI para continuar.")
                        st.stop()
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    
                    
                    client = OpenAI(api_key=openai_api_key)
                    try:
                        response = client.chat.completions.create(
                            model=CHATBOT_MODEL,
                            messages=[
                                {"role": m["role"], "content": m["content"]}
                                for m in st.session_state.messages
                            ]
                        )
                        msg = response.choices[0].message.content
                        st.session_state.messages.append({"role": "assistant", "content": msg})
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error al comunicarse con OpenAI: {str(e)}")

                st.markdown("""
                    <script>
                        const chatContainer = document.querySelector('.chat-container');
                        if (chatContainer) {
                            chatContainer.scrollTop = chatContainer.scrollHeight;
                        }
                    </script>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error al cargar el mapa de puntos: {str(e)}")