import requests
import os
from google import genai
from google.genai import types
class LargeLanguageModelGemini:
    model = "gemini-2.0-flash-001"
    google_api_key = "GEMINI_API_KEY"
    system_prompt = ""
    def load_environment(self):
        self.google_api_key = os.getenv('GEMINI_API_KEY')
        if self.google_api_key:
            print(f"Google API Key exists and begins {self.google_api_key[:8]}")
        else:
            print("Google API Key not set")
        print(f"{self.google_api_key}")

    def call_model(self, message) -> str:
        """Method to call the Gemini LLM with a message and return the response"""
        client = genai.Client(api_key= self.google_api_key)
        # Convert history to a single string for the model

        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=message,
            config=types.GenerateContentConfig(
            system_instruction=[self.system_prompt]
            )
        )
        return response.text
    def __init__(self,system_prompt: str = ""):
        self.system_prompt = system_prompt
        self.load_environment()



