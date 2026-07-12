import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(BASE_DIR, '.env')
load_dotenv(env_path)
class Config:
    # Server config
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', 5000))
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 't')

    # Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # Assuming the app is run from backend folder, but the legacy app expects paths relative to CWD.
    # We will make paths absolute based on BASE_DIR to ensure robustness.
    CONTENT_DIR = os.path.join(BASE_DIR, os.getenv('CONTENT_DIR', 'content'))
    TEMP_DIR = os.path.join(BASE_DIR, os.getenv('TEMP_DIR', 'temp'))
    OUTPUT_DIR = os.path.join(BASE_DIR, os.getenv('OUTPUT_DIR', 'output'))
    QUIZ_DIR = os.path.join(BASE_DIR, os.getenv('QUIZ_DIR', 'quiz_out'))
    

    # AI Config
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    DEFAULT_QUESTION_COUNT = int(os.getenv('DEFAULT_QUESTION_COUNT', 10))
    
    @classmethod
    def get_directories(cls):
        """Returns a list of all required working directories."""
        return [cls.CONTENT_DIR, cls.TEMP_DIR, cls.OUTPUT_DIR, cls.QUIZ_DIR]
