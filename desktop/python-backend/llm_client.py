import google.generativeai as genai
from config import Config

def get_vision_model():
    """Returns a configured Gemini GenerativeModel for vision inference."""
    genai.configure(api_key=Config.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-3.1-flash-lite')
    return model

def get_quiz_model():
    """Returns a configured Gemini GenerativeModel for quiz generation with JSON output."""
    genai.configure(api_key=Config.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-3.1-flash-lite', generation_config={"response_mime_type": "application/json"})
    return model
