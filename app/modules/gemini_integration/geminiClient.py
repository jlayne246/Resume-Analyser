from google import genai
import os

class GeminiClient:
    """A client to interact with Gemini models for content generation.
    Attributes:
        client (genai.Client): The Gemini API client initialized with the API key.
    """
    def __init__(self):
        """Initializes the GeminiClient with the API key from environment variables."""
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    def askFlash2(self,query:str)->str:
        """Asks Gemini Flash 2.0 model a question and returns the response as a string.
        
        Args:
            query (string): The question to ask the model.

        Returns:
            response (string): The model's response.
        """
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=query
        )
        return response.text
    def askFlash2_5(self,query:str)->str:
        """Asks Gemini Flash 2.0 model a question and returns the response as a string.
        
        Args:
            query (string): The question to ask the model.

        Returns:
            response (string): The model's response.
        """
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=query
        )
        return response.text
