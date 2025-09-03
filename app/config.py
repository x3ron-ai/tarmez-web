from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
	secret_key: str = os.getenv("SECRET_KEY", "change_me")
	api_url: str = os.getenv("API_URL", "http://localhost:8000")

settings = Settings()