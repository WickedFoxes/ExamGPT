from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

import tiktoken

class GPT:
    def __init__(self):
        OpenAI.api_key = os.environ.get('OPENAI_API_KEY')
        self.client = OpenAI()
        self.messages = []
    
    def add_message(self, role, content):
        message = {"role" : role, "content" : content}
        self.messages.append(message)

    def add_vision_message(self, role, type, content):
        if(type == "text"):
            message = {
                "role" : role, 
                "content" : [{"type": "text", "text": content}]
            }
        if(type == "image_url"):
            message = {
                "role" : role, 
                "content" : [{"type": "image_url", "image_url": {"url" : content}}]
            }
        self.messages.append(message)

    def get_gpt3_json(self):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=self.messages
        )
        return response.choices[0].message.content
    
    def get_gpt4_text(self):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            # model="gpt-4-turbo",
            messages=self.messages
        )
        return response.choices[0].message.content

    def get_gpt4_json(self):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            # model="gpt-4-turbo",
            response_format={ "type": "json_object" },
            messages=self.messages
        )
        return response.choices[0].message.content

    def get_gpt4_vision(self):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=self.messages
        )
        return response.choices[0].message.content
    
class Token:
    def __init__(self, texts):
        self.texts = texts

    def gpt4_token_count(self):
        return len(self.tokenizer('gpt-4'))

    def encoding_getter(self, type):
        return tiktoken.encoding_for_model(type)
    
    def tokenizer(self, type):
        encoding = self.encoding_getter(type)
        tokens = encoding.encode(self.texts)
        return tokens