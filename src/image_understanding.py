import os
import requests
from capture_snapshot import capture_screenshot_as_base64
import asyncio


class VisionModelProcessor:
    
    def __init__(
        self,
        url: str,
        openai_api_key: str,
        llm_model: str
    ) -> None:
        self.url = url
        self.__api_key = ""
        self.__llm_model = "gpt-4o-mini"
    
    
    def _encode_image(
        self
    ):
        base64_image = asyncio.run(capture_screenshot_as_base64(self.url))
        return base64_image
    
    
    def execute(
        self,
        user_message=str
    ) -> str:
        
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.__api_key}"
        }

        payload = {
            "model": self.__llm_model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_message
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{self._encode_image()}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        print(response.status_code)
        
        response = response.json()
        return response["choices"][0]["message"].get("content","No hay una respuesta, Error")
    
