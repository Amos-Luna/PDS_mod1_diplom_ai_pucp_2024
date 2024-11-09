import streamlit as st
from openai import OpenAI
from constants import CHATBOT_MODEL
from pydantic import BaseModel, ConfigDict
from utils import get_full_text_from_images

class Chatbot(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def render(self):
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
                padding: 20px;
            }
            .chat-content {
                display: flex;
                flex-direction: column;
                gap: 20px;
                height: 100%;
            }
            .message-container {
                background-color: #262730;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 10px;
            }
            .insights-title {
                margin-bottom: 10px;
                color: #ffffff;
            }
            .insights-content {
                color: #e0e0e0;
                line-height: 1.5;
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.subheader('CHAT BRAIN - Interpretador Agil de Datos e Insights')
        
        st.session_state.openai_api_key = st.text_input("**INSERT YOUR OPENAI_API_KEY** 👇", key="chatbot_api_key", type="password")
        if not st.session_state.openai_api_key:
            st.info("Por favor, añade tu API key de OpenAI para continuar.")
            st.stop()
        
        messages_container = st.container(height=750)
        
        with messages_container:
            
            client = OpenAI(api_key=st.session_state.openai_api_key)
            
            try:
                full_text_interpreted = get_full_text_from_images(temp_image_paths = st.session_state.plot_analytics_paths)
                response = client.chat.completions.create(
                    model=CHATBOT_MODEL,
                    messages=[
                        {"role": "system", "content": "Build a summary less than 4 paragraphs in Spanish"},
                        {
                            "role": "user",
                            "content": full_text_interpreted
                        }
                    ]
                )
                
                msg_result = response.choices[0].message.content
                st.markdown(
                    f'<div class="message-container">'
                    f'<h3 class="insights-title">Insights encontrados del Dashboard:</h3>'
                    f'<div class="insights-content">{msg_result}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

            except Exception as e:
                st.error(f"Error al comunicarse con OpenAI: {str(e)}")
        