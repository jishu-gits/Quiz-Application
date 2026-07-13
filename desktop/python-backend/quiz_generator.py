import os
import json
from config import Config
from utils import logger
from llm_client import get_quiz_model

def generate_quiz_json(input_text: str, num_questions: int = None) -> str:
    """
    Generates quiz questions from the provided input text.
    Instructs the LLM to return valid JSON matching the existing API contract.
    
    Args:
        input_text: The merged text extracted from the vision model.
        num_questions: Number of questions to generate (defaults to Config).
        
    Returns:
        str: The raw JSON string returned by the model.
        
    Raises:
        Exception: If the LLM call fails or the output cannot be parsed.
    """
    if num_questions is None:
        num_questions = Config.DEFAULT_QUESTION_COUNT
        
    logger.info(f"Generating {num_questions} quiz questions via LLM...")
    
    prompt = f"""You are an edututor substitute model, whose function is to create quizzes. You will receive a query. This query is an output from a Vision Model.
Clean the text to remove irrelevant data, and generate {num_questions} quiz questions from the given data.
You must not only generate a question and subsequent 4 options, but also one of the option must be true. You must also return 1 correct option from the given options, and explaination if possible. return NA if no explaination.
Return the output as valid JSON in the following format:
{{
   "questions": [
     {{
        "question": "Question text",
        "options": [provide 4 options here],
        "answer": provide the answer here
     }}
     // Repeat for each question
   ]
}}
Ensure the JSON is valid.
"""

    model = get_quiz_model()
    
    full_prompt = prompt + "\n\nInput Text:\n" + input_text
    
    response = model.generate_content(full_prompt)
    quiz_json_string = response.text
    
    # We perform a quick sanity check to ensure the LLM actually returned JSON
    # If it didn't, this will throw an exception caught below.
    try:
        # We don't return the dict, we return the string, but we want to fail fast if it's garbage.
        # Sometimes LLMs wrap json in markdown ```json ... ``` blocks.
        cleaned_json = quiz_json_string.strip()
        if cleaned_json.startswith('```json'):
            cleaned_json = cleaned_json[7:]
        if cleaned_json.endswith('```'):
            cleaned_json = cleaned_json[:-3]
        cleaned_json = cleaned_json.strip()
            
        json.loads(cleaned_json) 
        quiz_json_string = cleaned_json
    except json.JSONDecodeError as je:
        logger.warning(f"LLM output might not be pure JSON. Error: {je}")
        # We fall back to the raw string in case the Java client handles it
        
    # Save to disk to satisfy the GET endpoint logic
    quiz_file = os.path.join(Config.QUIZ_DIR, "latest_quiz.json")
    with open(quiz_file, "w", encoding='utf-8') as fout:
        fout.write(quiz_json_string)
        
    logger.info("Quiz questions successfully generated and saved.")
    return quiz_json_string
