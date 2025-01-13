import requests
from config import settings

class OllamaClient:
    def __init__(self):
        self.api_url = settings.OLLAMA_API_URL
    
    async def generate_response(self, prompt: str) -> str:
        try:
            system_prompt = """
            \n\nYou are an AI Assistant Sage create by Mayank Patel. Your task is to help users answer questions.

The following questions are to be used a guide when generating a response.

{question}

Always respond with the most accurate and concise information possible. If you are unsure about the answer, please let the user know.

Always answer questions as Sage.

""".format(question=prompt)
            response = requests.post(
                self.api_url,
                json={
                    "model": "phi4",
                    "prompt": system_prompt,
                    "stream": False
                }
            )
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Sorry, I'm having trouble processing your request."
