from google import genai
import os
import sys
from pathlib import Path

# No hardcoding: expect GENAI_API_KEY in environment
api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    print("ERROR: set GENAI_API_KEY environment variable", file=sys.stderr)
    sys.exit(1)

client = genai.Client(api_key=api_key)

# System prompt for Student Services Bot
system_prompt = """
Ты бот для поддержки студентов. Твоя задача:
1) Помогать со сбросом пароля
2) Помогать с регистрацией на курсы

Отвечай как вежливый помощник студента. Будь полезным и избегай грубых слов.
"""

# User message (from env or argument)
user_message = os.getenv("USER_MESSAGE", "Hello, I need help with my account.")

# Form the full prompt
full_prompt = f"{system_prompt}\n\nПользователь спрашивает: {user_message}\n\nОтвет:"

try:
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=full_prompt
    )
    text = getattr(response, "text", str(response)).strip()
    print(text)

    # Optionally: save transcript if TRANSCRIPT_PATH is set
    transcript_path = os.getenv("TRANSCRIPT_PATH")
    if transcript_path:
        p = Path(transcript_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "a", encoding="utf-8") as f:
            f.write(f"USER: {user_message}\n")
            f.write(f"BOT: {text}\n")
            f.write("-" * 50 + "\n")
except Exception as e:
    print("Request failed:", e, file=sys.stderr)
    sys.exit(1)
