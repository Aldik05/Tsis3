# Простой пример: загружает synthetic_dataset.jsonl, вызывает агент и оценивает по простым правилам
import json
from pathlib import Path
from google import genai
import os
import sys
import csv

DATA = Path("data/synthetic_dataset.jsonl")
RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    print("ERROR: set GENAI_API_KEY environment variable", file=sys.stderr)
    sys.exit(1)

client = genai.Client(api_key=api_key)

if not DATA.exists():
    print(f"ERROR: dataset not found at {DATA}", file=sys.stderr)
    sys.exit(1)

# Системный промпт для Student Services Bot
system_prompt = """
Ты бот для поддержки студентов. Твоя задача:
1) Помогать со сбросом пароля
2) Помогать с регистрацией на курсы

Отвечай как вежливый помощник студента. Будь полезным и избегай грубых слов.
"""

results = []
for line in DATA.read_text().strip().splitlines():
    try:
        item = json.loads(line)
    except json.JSONDecodeError as e:
        print(f"Skipping invalid JSON: {e}", file=sys.stderr)
        continue
    
    # Берём только последний пользовательский вопрос из conversation
    user_question = ""
    for msg in reversed(item.get('conversation', [])):
        if msg['role'] == 'user':
            user_question = msg['text']
            break
    
    full_prompt = f"{system_prompt}\n\nПользователь спрашивает: {user_question}\n\nОтвет:"
    
    try:
        resp = client.models.generate_content(model="gemini-2.0-flash-001", contents=full_prompt)
        text = getattr(resp, "text", str(resp)).strip()
    except Exception as e:
        text = f"<error: {e}>"
    
    expected = (item.get("expected") or "").lower()
    correct = expected and expected in text.lower()
    blacklist = ["stupid", "idiot", "dumb"]
    polite = all(bad not in text.lower() for bad in blacklist)
    
    results.append({
        "id": item.get("id"),
        "jtbd": item.get("jtbd"),
        "correct": bool(correct),
        "polite": bool(polite),
        "reply": text
    })

# Save JSONL
with open(RESULTS_DIR / "results.jsonl", "w", encoding="utf-8") as f:
    for r in results:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

# Save CSV summary
with open(RESULTS_DIR / "results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "jtbd", "correct", "polite", "reply"])
    writer.writeheader()
    for r in results:
        writer.writerow(r)

# Print summary
total = len(results)
passed = sum(1 for r in results if r["correct"] and r["polite"])
print(f"\n=== EVAL SUMMARY ===")
print(f"Total: {total}")
print(f"Passed (correct & polite): {passed}/{total}")
print(f"Results saved to {RESULTS_DIR}/")