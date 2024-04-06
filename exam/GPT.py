from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

class GPT:
    def __init__(self):
        OpenAI.api_key = os.environ.get('OPENAI_API_KEY')
        self.client = OpenAI()
        self.messages = []
    
    def add_message(self, role, content):
        message = {"role" : role, "content" : content}
        self.messages.append(message)

    def get_gpt3_json(self):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=self.messages
        )
        return response.choices[0].message.content
    
    def get_gpt4_json(self):
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            response_format={ "type": "json_object" },
            messages=self.messages
        )
        return response.choices[0].message.content

    def get_gpt4_vision(self, image_url):
        response = self.client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages = [{
                "role": "user",
                "content": [
                {
                    "type": "text",
                    "text": "What's in this image?"
                },
                {
                    "type": "image_url",
                    "image_url": {
                    "url": f"{image_url}"
                    }
                }
                ]
            }],
        )
        return response.choices[0].message.content