# eval_correctness.py
# Шаблон eval для проверок корректности ответа: ищем ключевые слова из поля "expected".
# Использование:
# 1) Убедитесь, что у вас есть файл с ответами модели: results/results_mock.jsonl или results/results.jsonl
#    Формат строки: {"id": "<id>", "response": "<текст ответа>"}
# 2) Запуск из корня проекта:
#    python3 evals/eval_correctness.py --dataset data/synthetic_dataset.jsonl --responses results/results_mock.jsonl --out results/eval_correctness.jsonl
import json
import argparse
from pathlib import Path
import csv
import re

def parse_response_obj(obj):
    # Поддерживаем разные форматы ответа (строка, dict с text/outputs/candidates)
    if isinstance(obj, str):
        return obj.strip()
    if hasattr(obj, "text"):
        return str(getattr(obj, "text")).strip()
    if isinstance(obj, dict):
        if "text" in obj and isinstance(obj["text"], str):
            return obj["text"].strip()
        if "output" in obj and isinstance(obj["output"], str):
            return obj["output"].strip()
        if "outputs" in obj and obj["outputs"]:
            first = obj["outputs"][0]
            return str(first.get("content", first) if isinstance(first, dict) else first).strip()
        if "candidates" in obj and obj["candidates"]:
            cand = obj["candidates"][0]
            return str(cand.get("content", cand) if isinstance(cand, dict) else cand).strip()
    return str(obj).strip()

def check_expected_in_response(response_text, expected_list):
    text = response_text.lower()
    for token in expected_list:
        if token.lower() in text:
            return True
    return False

def load_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dataset", required=True)
    p.add_argument("--responses", required=True)
    p.add_argument("--out", default="results/eval_correctness.jsonl")
    args = p.parse_args()

    dataset = {item["id"]: item for item in load_jsonl(args.dataset)}
    responses = {item["id"]: item for item in load_jsonl(args.responses)}

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    csv_rows = []
    with open(out_path, "w", encoding="utf-8") as out_f:
        for id_, data in dataset.items():
            expected = data.get("expected", [])
            resp_obj = responses.get(id_, {}).get("response", "")
            resp_text = parse_response_obj(resp_obj)
            passed = check_expected_in_response(resp_text, expected)
            record = {"id": id_, "jtbd": data.get("jtbd"), "expected": expected, "response": resp_text, "pass": passed}
            out_f.write(json.dumps(record, ensure_ascii=False) + "\n")
            csv_rows.append(record)

    # Записать CSV
    csv_path = out_path.with_suffix(".csv")
    with open(csv_path, "w", encoding="utf-8", newline="") as csvf:
        writer = csv.DictWriter(csvf, fieldnames=["id","jtbd","expected","response","pass"])
        writer.writeheader()
        for r in csv_rows:
            writer.writerow(r)

if __name__ == "__main__":
    main()