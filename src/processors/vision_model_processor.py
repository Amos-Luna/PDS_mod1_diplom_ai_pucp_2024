import streamlit as st
import requests
import base64
from processors.prompt_template import InsightsPromptFinder
from constants import CHATBOT_MODEL


class VisionModelProcessor:

    def __init__(self) -> None:
        self.__api_key = st.session_state.openai_api_key
        self.__llm_model = CHATBOT_MODEL


    def _encode_image(
        self, 
        image_path: str
    ):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")


    def extract_text_from_image(
        self, 
        image_path: str
    ) -> str:

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.__api_key}",
        }

        payload = {
            "model": self.__llm_model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": InsightsPromptFinder.system_prompt.template},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{self._encode_image(image_path)}"
                            },
                        },
                    ],
                }
            ],
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions", 
            headers=headers, 
            json=payload
        )
        
        response = response.json()
        return response["choices"][0]["message"].get("content", "")
