from google import genai
import os

class GeminiClient:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))
    def askFlash2(self,query:str)->str:
        response = self.client.models.generate_content(
        model="gemini-2.0-flash",
        contents=query
        )
        return response.text
    def askFlash2_5(self,query:str)->str:
        response = self.client.models.generate_content(
        model="gemini-2.5-flash",
        contents=query
        )
        return response.text
