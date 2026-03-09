import google.generativeai as genai
from app.core.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)


class GeminiLLM:

    def __init__(self):

        self.model = genai.GenerativeModel("gemini-3-flash-preview")

    def generate(self, prompt):

        response = self.model.generate_content(prompt)

        return response.text
