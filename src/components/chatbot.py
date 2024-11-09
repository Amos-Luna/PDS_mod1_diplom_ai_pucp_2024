# src/chatbot.py
import streamlit as st
from openai import OpenAI
from constants import CHATBOT_MODEL
from pydantic import BaseModel, ConfigDict


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