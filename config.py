from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    WHATSAPP_TOKEN: str
    VERIFY_TOKEN: str
    OLLAMA_API_URL: str = "http://localhost:11434/api/generate"
    PHONE_NUMBER_ID: str
    
    class Config:
        env_file = ".env"

settings = Settings()