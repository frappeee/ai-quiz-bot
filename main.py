import os
import json
import requests
from dotenv import load_dotenv
from typing import List, Dict, Optional

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def generate_quiz(topic: str, number_of_questions: int = 5) -> Optional[List[Dict[str, str]]]:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "AI Quiz App"
    }

    prompt = f"""Generate {number_of_questions} multiple-choice quiz questions about '{topic}'.
Each question must have:
- 'q': The question text
- 'A': Option A
- 'B': Option B
- 'C': Option C
- 'D': Option D
- 'correct': The correct answer (A, B, C, or D)
Return ONLY a valid JSON array of these objects, nothing else."""

    body = {
        "model": "openai/gpt-3.5-turbo",
       
