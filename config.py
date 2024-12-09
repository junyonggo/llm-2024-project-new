# config.py

import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Add your API key to .env
    MODEL_NAME = "gpt-4o-2024-08-06"
    MAX_TOKENS = 1000
    TEMPERATURE = 0.7
    IMAGE_SIZE = "1024x1024"