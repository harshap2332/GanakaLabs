import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    DATABASE_URL = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = os.getenv('DEBUG', 'false') == 'true'